# <img src="/AvengersAssemble/tixx/static/images/tixxlogopng.png" alt="Tixx Logo" width="200" height="120">

Tixx is a web application designed to streamline the organization and attendance of events. It facilitates easy event discovery, registration, and ticket purchasing for users, while providing organizers with tools for event creation, management, and promotion. The platform enhances engagement through personalized user experiences and ensures secure transactions.

## Tixx - Features

1. **Home Page**
   - The Home Page serves as an engaging entry point to key events and influential figures. It's equipped with an intuitive, advanced search feature and provides clear guidance for new users to either register or log in, ensuring a seamless introduction to the platform.

2. **Search Functionality**
   - The Search Results Page allows users to dynamically explore events, figures, and genres through detailed queries, offering a tailored exploration experience based on specific interests or criteria.

3. **User Account Management**
   - Offers streamlined processes for user registration and login, facilitating the tracking of personal preferences and management of specific data such as ticket purchases, reviews, and personal details.

4. **Event Organiser Access**
   - Provides a dedicated portal for event organisers to register and log in, enabling them to submit new events for review, track the status of these events, and manage their profiles and personal information.

5. **Event Submission**
   - Organisers can create comprehensive event listings, specifying key details such as dates, times, locations, venues, genres, and status, enriching the platform's diversity of offerings.

6. **Ticketing Process**
   - Enables users to seamlessly select and secure tickets for events, with a dynamic reservation system that confirms seats upon payment.

7. **Secure Payment Gateway**
   - Leverages the Stripe API for ticket purchases, ensuring transaction security and providing users with a variety of payment options.

8. **Admin Review**
   - Administrators have the ability to review, approve, reject, edit, and delete event submissions from organisers, maintaining the platform's integrity by ensuring that only legitimate content is published.

9. **Profile Management**
   - Supports user engagement and personalization by allowing users to view and edit their profiles, set preferences, and review past activities.

10. **Confirmation and Notifications**
    - Users receive immediate confirmation of successful transactions, complete with detailed information about their purchase, including seat assignments, event dates, and payment details.

## Tixx - Setup

### Prerequisites

- Python 3.x
- pip
- Virtual environment (recommended)

### Installation Steps

1. **Clone the Repository**
   - Run `git clone https://github.com/olivernicholass/TIXX.git` and navigate into the project directory with `cd AvengersAssemble`.

2. **Set Up a Virtual Environment (Optional but Recommended)**
   - On Unix/macOS: Execute `python3 -m venv venv` followed by `source venv/bin/activate`.
   - On Windows: Use `python -m venv venv` then `.\venv\Scripts\activate`.

3. **Install Required Dependencies**
   - Install all dependencies with `pip install -r requirements.txt`.

4. **Configure the Project Settings**
   - Make necessary adjustments in the `settings.py` file to match your environment setup, such as database configurations.

5. **Database Setup**
   - Run `python manage.py makemigrations` and `python manage.py migrate` to set up your database structure.

6. **Launch the Application**
   - Start the project with `python manage.py runserver` and visit `http://127.0.0.1:8000/` in your browser to view it.

### Registering an Admin

- To access the admin site, you'll need to create an admin user. Run `python manage.py createsuperuser` and follow the prompts.
