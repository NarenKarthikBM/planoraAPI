# PlanoraAPI

## Overview

The **PlanoraAPI** is a web-based application designed to facilitate seamless event organization and browsing events. It provides a structured workflow for event creation, attendee interaction. The platform includes modules for event organizer dashboard, attendees live feed, metric trackers, and common features such as calendar integration.

## Features

### Organizer Module

- **Event Management Page**: Organizers can create and manage event pages with essential details like event name, date, time, location, and description.
- **Management of Attendees**: Organizers can track RSVPs, view attendee metrics, and manage event participation.
- **Attendee Metrics & Tracker**: A built-in system to monitor event engagement using QR based tracking.
- **Event Feedback**: Collect feedback from attendees to improve future events.

### Engagement Module

- **Event Feed**: A centralized page where attendees can see live event feed.
- **Page Interaction**: Users can engage with event content through likes & sharing options.
- **Calendar Sync**: Integration with Google Calendar.

### Attendee Module

- **Event Filter & Search**: Find events based on categories, location, and date.
- **RSVP**: Confirm participation by clicking i'm interested button.
- **Calendar Integration**: Add events directly to personal calendars.

## Tech Stack

- **Frontend**: Next.js (React.js)
- **Backend**: Django
- **Database**: MySQL
- **Authentication**: Custom Token based 
- **Notifications**: Email notifications
- **Deployment**: PythonAnywhere & Vercel App

## Installation & Setup

### Prerequisites

- MySQL
- Django
- Git
- Python 3.10+

### Steps to Run Locally

1. **Clone the repository**
   ```sh
   git clone https://github.com/NarenKarthikBM/planoraAPI.git
   ```
2. **Install dependencies**
   ```sh
   npm install requirements.txt
   ```
3. **Set up environment variables** (Create a `.env` file and add required keys)
   ```sh
   DATABASE_URL=mongodb://localhost:27017/eventDB
   JWT_SECRET=your_secret_key
   ```
4. **Run the application**
   ```sh
   npm start
   ```
5. **Access the platform**
   Open `http://localhost:3000` in your browser.

## API Endpoints

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| POST   | `/api/auth/register`   | Register a new user |
| POST   | `/api/auth/login`      | Authenticate user   |
| POST   | `/api/events`          | Create a new event  |
| GET    | `/api/events`          | Fetch all events    |
| GET    | `/api/events/:id`      | Fetch event details |
| POST   | `/api/events/:id/rsvp` | RSVP to an event    |
| DELETE | `/api/events/:id`      | Delete an event     |

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

No License

## Contact

For any queries or suggestions, feel free to reach out:

- GitHub: [PlanoraAPI](https://github.com/NarenKarthikBM/planoraAPI)

