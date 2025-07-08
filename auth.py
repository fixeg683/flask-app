from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from urllib.parse import urlparse
import re

from app import db, mail
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(to, subject, template, **kwargs):
    """Send email using Flask-Mail"""
    try:
        # Check if email is configured
        if not current_app.config.get('MAIL_USERNAME'):
            print("Email not configured - skipping email send")
            return False
            
        msg = Message(
            subject=subject,
            recipients=[to],
            html=template,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
            return render_template('auth/signup.html')
        
        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/signup.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/signup.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/signup.html')
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        
        # Generate confirmation token
        token = user.generate_confirmation_token()
        
        db.session.add(user)
        db.session.commit()
        
        # Send confirmation email
        confirmation_url = url_for('auth.confirm_email', token=token, _external=True)
        email_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">Welcome to Digital Store!</h2>
            <p>Thank you for signing up. Please click the button below to confirm your email address:</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{confirmation_url}" 
                   style="background-color: #007bff; color: white; padding: 12px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Confirm Email
                </a>
            </p>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p><a href="{confirmation_url}">{confirmation_url}</a></p>
            <p>This link will expire in 24 hours.</p>
        </div>
        """
        
        if send_email(email, 'Confirm Your Email - Digital Store', email_html):
            flash('Registration successful! Please check your email to confirm your account.', 'success')
            return redirect(url_for('auth.login'))
        else:
            # Auto-confirm user if email sending fails (development mode)
            user.is_confirmed = True
            db.session.commit()
            flash('Registration successful! Your account has been automatically confirmed.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username.lower())
        ).first()
        
        if user and user.check_password(password):
            # Skip email confirmation check if email is not configured
            if not user.is_confirmed and current_app.config.get('MAIL_USERNAME'):
                flash('Please confirm your email address before logging in.', 'warning')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page and urlparse(next_page).netloc == '':
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@bp.route('/confirm/<token>')
def confirm_email(token):
    """Confirm email address"""
    user = User.query.filter_by(confirmation_token=token).first()
    
    if not user:
        flash('Invalid or expired confirmation link.', 'error')
        return redirect(url_for('auth.login'))
    
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'info')
        return redirect(url_for('auth.login'))
    
    user.is_confirmed = True
    user.confirmation_token = None
    db.session.commit()
    
    flash('Email confirmed successfully! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = user.generate_reset_token()
            db.session.commit()
            
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            email_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Password Reset - Digital Store</h2>
                <p>We received a request to reset your password. Click the button below to reset it:</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background-color: #dc3545; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Reset Password
                    </a>
                </p>
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p><a href="{reset_url}">{reset_url}</a></p>
                <p>This link will expire in 24 hours.</p>
                <p>If you did not request this reset, please ignore this email.</p>
            </div>
            """
            
            send_email(email, 'Reset Your Password - Digital Store', email_html)
        
        # Always show success message for security
        flash('If an account with that email exists, we have sent a password reset link.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.is_reset_token_valid():
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/reset_password.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html')
        
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        
        flash('Password reset successful! You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html')

@bp.route('/resend-confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    """Resend confirmation email"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/resend_confirmation.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and not user.is_confirmed:
            token = user.generate_confirmation_token()
            db.session.commit()
            
            confirmation_url = url_for('auth.confirm_email', token=token, _external=True)
            email_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Confirm Your Email - Digital Store</h2>
                <p>Please click the button below to confirm your email address:</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{confirmation_url}" 
                       style="background-color: #007bff; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Confirm Email
                    </a>
                </p>
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p><a href="{confirmation_url}">{confirmation_url}</a></p>
                <p>This link will expire in 24 hours.</p>
            </div>
            """
            
            send_email(email, 'Confirm Your Email - Digital Store', email_html)
        
        # Always show success message for security
        flash('If an unconfirmed account with that email exists, we have sent a confirmation link.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/resend_confirmation.html')

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html')

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password for logged-in user"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')