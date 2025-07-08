# Digital Store - E-commerce Platform

## Overview

This is a Flask-based e-commerce platform for digital products including movies, software, and games. The application provides a complete shopping experience with product browsing, cart management, and PayPal checkout integration.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with PostgreSQL (production database)
- **Session Management**: Flask sessions for cart persistence
- **Payment Processing**: PayPal SDK integration with sandbox credentials
- **Environment Configuration**: Environment variables for sensitive data
- **Image Sources**: TMDB for movies, Icons8 for software, RAWG for games

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6
- **JavaScript**: Vanilla JS for cart functionality and PayPal integration
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Database Schema
- **Products**: Central product catalog with category-specific fields
- **CartItems**: Session-based shopping cart storage
- **Orders**: Order tracking and history (referenced but not fully implemented)
- **Categories**: Enum-based categorization (MOVIE, SOFTWARE, GAME)

## Key Components

### Models (models.py)
- **Product Model**: Flexible product structure supporting multiple categories with category-specific fields (director for movies, platform for software/games)
- **CartItem Model**: Session-based cart items linked to products
- **CategoryType Enum**: Defines available product categories
- **Order/OrderItem Models**: Referenced for future order management
- **User Model**: Complete authentication system with password hashing, email confirmation, and password reset tokens

### Authentication System (auth.py)
- **User Registration**: Sign up with email confirmation
- **Login/Logout**: Secure session management with Flask-Login
- **Password Reset**: Email-based password recovery system
- **Email Confirmation**: Account activation via email links
- **Profile Management**: User profile and password change functionality
- **Development Mode**: Automatic confirmation when email is not configured

### Routes (routes.py)
- **Home Route**: Featured products display across all categories
- **Category Routes**: Filtered product listings with search and sorting
- **Product Detail Routes**: Individual product pages
- **Cart Management**: Add, update, remove cart items
- **Checkout Flow**: PayPal integration for payment processing

### Templates
- **Base Template**: Consistent layout with navigation and footer
- **Product Listings**: Grid-based product display with filtering
- **Shopping Cart**: Cart management with quantity controls
- **Checkout Process**: Multi-step checkout with PayPal integration

## Data Flow

1. **Product Browsing**: Users browse categories or search products
2. **Cart Management**: Products added to session-based cart
3. **Checkout Process**: Users review order and complete PayPal payment
4. **Order Processing**: Successful payments trigger order creation
5. **Mock Data**: Development environment uses predefined product data

## External Dependencies

### Payment Processing
- **PayPal SDK**: JavaScript SDK for payment processing
- **PayPal REST API**: Server-side payment validation
- **Sandbox Environment**: Development and testing support

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme
- **Font Awesome 6**: Icon library
- **PayPal JavaScript SDK**: Payment button integration

### Python Packages
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Werkzeug**: WSGI utilities and proxy fix

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database, debug mode enabled
- **Production**: PostgreSQL database, environment-based secrets
- **PayPal Integration**: Sandbox for development, live for production

### Security Considerations
- **Session Management**: Secure session keys
- **Proxy Configuration**: ProxyFix for reverse proxy deployment
- **Database Security**: Parameterized queries through SQLAlchemy ORM

### Scalability Features
- **Database Connection Pooling**: Configured for production workloads
- **Session-based Cart**: Reduces database writes
- **Pagination**: Efficient product listing for large catalogs

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- July 03, 2025: Initial setup with Flask e-commerce platform
- July 03, 2025: Added PostgreSQL database integration
- July 03, 2025: Implemented real product images from TMDB, Icons8, and RAWG APIs
- July 03, 2025: Added error handling templates (404, 500)
- July 04, 2025: Implemented complete user authentication system with signup, login, password reset, and email confirmation
- July 04, 2025: Added user profile management and secure session handling
- July 04, 2025: Integrated authentication with existing navigation and shopping cart system
- July 08, 2025: Migrated project from Replit Agent to Replit environment
- July 08, 2025: Fixed circular import issues and database configuration
- July 08, 2025: Created essential HTML templates for proper functionality
- July 08, 2025: Integrated OpenAI-powered customer support chatbot with GPT-4o
- July 08, 2025: Added floating chat widget with quick support options
- July 08, 2025: Implemented sentiment analysis for support ticket prioritization