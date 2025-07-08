from app import db
from models import Product, CategoryType
from datetime import date

def initialize_mock_data():
    """Initialize the database with mock product data"""
    # Check if data already exists
    if Product.query.count() > 0:
        return
    
    # Movies
    movies = [
        Product(
            title="The Matrix",
            description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            price=14.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            release_date=date(1999, 3, 31),
            rating=8.7,
            genre="Action, Sci-Fi",
            director="The Wachowskis"
        ),
        Product(
            title="Inception",
            description="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            price=12.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            release_date=date(2010, 7, 16),
            rating=8.8,
            genre="Action, Sci-Fi, Thriller",
            director="Christopher Nolan"
        ),
        Product(
            title="The Dark Knight",
            description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
            price=13.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            release_date=date(2008, 7, 18),
            rating=9.0,
            genre="Action, Crime, Drama",
            director="Christopher Nolan"
        ),
        Product(
            title="Pulp Fiction",
            description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
            price=11.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            release_date=date(1994, 10, 14),
            rating=8.9,
            genre="Crime, Drama",
            director="Quentin Tarantino"
        ),
        Product(
            title="Avatar",
            description="A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
            price=15.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg",
            release_date=date(2009, 12, 18),
            rating=7.8,
            genre="Action, Adventure, Fantasy",
            director="James Cameron"
        ),
        Product(
            title="Interstellar",
            description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            price=14.99,
            category=CategoryType.MOVIE,
            image_url="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            release_date=date(2014, 11, 7),
            rating=8.6,
            genre="Adventure, Drama, Sci-Fi",
            director="Christopher Nolan"
        )
    ]
    
    # Software
    software = [
        Product(
            title="Adobe Photoshop 2024",
            description="The world's best imaging and graphic design software. Create and enhance photographs, illustrations, and 3D artwork.",
            price=239.88,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/adobe-photoshop.png",
            release_date=date(2023, 10, 1),
            rating=4.5,
            genre="Graphics, Design",
            platform="Windows, Mac",
            developer="Adobe Systems"
        ),
        Product(
            title="Microsoft Office 365",
            description="Get premium versions of Word, Excel, PowerPoint, and Outlook, plus 1TB of OneDrive cloud storage.",
            price=99.99,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/microsoft-office-2019.png",
            release_date=date(2023, 9, 1),
            rating=4.3,
            genre="Productivity, Office",
            platform="Windows, Mac, Web",
            developer="Microsoft"
        ),
        Product(
            title="Visual Studio Code",
            description="Free source-code editor made by Microsoft for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, and more.",
            price=0.00,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/visual-studio-code-2019.png",
            release_date=date(2023, 11, 1),
            rating=4.8,
            genre="Development, IDE",
            platform="Windows, Mac, Linux",
            developer="Microsoft"
        ),
        Product(
            title="Slack",
            description="A messaging app for business that connects people to the information they need. Transform how you work with one place for everyone and everything you need.",
            price=8.00,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/slack.png",
            release_date=date(2023, 8, 1),
            rating=4.2,
            genre="Communication, Business",
            platform="Windows, Mac, Web, Mobile",
            developer="Slack Technologies"
        ),
        Product(
            title="AutoCAD 2024",
            description="Computer-aided design software for 2D and 3D design and drafting. Used by architects, engineers, and construction professionals.",
            price=1690.00,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/color/300/autodesk-autocad.png",
            release_date=date(2023, 3, 1),
            rating=4.1,
            genre="CAD, Engineering",
            platform="Windows, Mac",
            developer="Autodesk"
        ),
        Product(
            title="Figma",
            description="A collaborative interface design tool. Design, prototype, and gather feedback all in one place with Figma.",
            price=12.00,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/figma.png",
            release_date=date(2023, 6, 1),
            rating=4.7,
            genre="Design, UI/UX",
            platform="Web, Desktop",
            developer="Figma Inc."
        ),
        Product(
            title="AnyDesk",
            description="Fast remote desktop software for secure connections to computers anywhere in the world. Perfect for remote work and support.",
            price=12.99,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/anydesk.png",
            release_date=date(2014, 8, 1),
            rating=4.3,
            genre="Remote Access, Productivity",
            platform="Windows, Mac, Linux, Mobile",
            developer="AnyDesk Software GmbH"
        ),
        Product(
            title="FileZilla",
            description="Free FTP solution for file transfers. Supports FTP, FTPS and SFTP protocols with an intuitive interface.",
            price=0.00,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/filezilla.png",
            release_date=date(2001, 1, 15),
            rating=4.5,
            genre="File Transfer, FTP",
            platform="Windows, Mac, Linux",
            developer="FileZilla Project"
        ),
        Product(
            title="Turbo C++",
            description="Classic C++ IDE and compiler perfect for learning programming. Includes debugging tools and code editor.",
            price=9.99,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/c-plus-plus-logo.png",
            release_date=date(1990, 5, 1),
            rating=4.1,
            genre="Development, IDE",
            platform="Windows, DOS",
            developer="Borland"
        ),
        Product(
            title="UltraViewer",
            description="Remote desktop software for technical support and remote access. Easy to use with secure connections.",
            price=19.99,
            category=CategoryType.SOFTWARE,
            image_url="https://img.icons8.com/fluency/300/remote-desktop.png",
            release_date=date(2017, 3, 10),
            rating=4.2,
            genre="Remote Access, Support",
            platform="Windows, Mac, Android, iOS",
            developer="DucFabulous Co."
        )
    ]
    
    # Games
    games = [
        Product(
            title="Cyberpunk 2077",
            description="An open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification.",
            price=59.99,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/26d/26d4437715bee60138dab4a7c8c59c92.jpg",
            release_date=date(2020, 12, 10),
            rating=7.2,
            genre="Action, RPG",
            platform="PC, PlayStation, Xbox",
            developer="CD Projekt Red"
        ),
        Product(
            title="The Witcher 3: Wild Hunt",
            description="A story-driven, next-generation open world role-playing game set in a visually stunning fantasy universe full of meaningful choices.",
            price=39.99,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/618/618c2031a07bbff6b4f611f10b6bcdbc.jpg",
            release_date=date(2015, 5, 19),
            rating=9.3,
            genre="Action, RPG",
            platform="PC, PlayStation, Xbox, Nintendo Switch",
            developer="CD Projekt Red"
        ),
        Product(
            title="Grand Theft Auto V",
            description="When a young street hustler, a retired bank robber and a terrifying psychopath find themselves entangled with some of the most frightening and deranged elements of the criminal underworld.",
            price=29.99,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/20a/20aa03a10cda45239fe22d035c0ebe64.jpg",
            release_date=date(2013, 9, 17),
            rating=8.7,
            genre="Action, Adventure",
            platform="PC, PlayStation, Xbox",
            developer="Rockstar Games"
        ),
        Product(
            title="Red Dead Redemption 2",
            description="America, 1899. The end of the Wild West era has begun. After a robbery goes badly wrong in the western town of Blackwater, Arthur Morgan and the Van der Linde gang are forced to flee.",
            price=59.99,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/511/5118aff5091cb3efec399c808f8c598f.jpg",
            release_date=date(2018, 10, 26),
            rating=9.7,
            genre="Action, Adventure",
            platform="PC, PlayStation, Xbox",
            developer="Rockstar Games"
        ),
        Product(
            title="Minecraft",
            description="A sandbox video game in which players explore a blocky, procedurally-generated 3D world, and may discover and extract raw materials, craft tools, and build structures.",
            price=26.95,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/b4e/b4e4c73d5aa4ec66bbf75375c4847a2b.jpg",
            release_date=date(2011, 11, 18),
            rating=8.0,
            genre="Sandbox, Survival",
            platform="PC, Mobile, Console",
            developer="Mojang Studios"
        ),
        Product(
            title="Elden Ring",
            description="A fantasy action-RPG adventure set within a world full of mystery and peril. Journey through the Lands Between, a new fantasy world created by Hidetaka Miyazaki.",
            price=59.99,
            category=CategoryType.GAME,
            image_url="https://media.rawg.io/media/games/5ec/5ecac5cb026ec26a56efcc546364e348.jpg",
            release_date=date(2022, 2, 25),
            rating=9.6,
            genre="Action, RPG",
            platform="PC, PlayStation, Xbox",
            developer="FromSoftware"
        )
    ]
    
    # Add all products to database
    for product_list in [movies, software, games]:
        for product in product_list:
            db.session.add(product)
    
    db.session.commit()
    print("Mock data initialized successfully!")
