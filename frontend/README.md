# Authentication Frontend

A React application implementing user authentication with Supabase.

## Features

- ✅ User login with email/password
- ✅ Session persistence across page refreshes
- ✅ Proper logout functionality
- ✅ Error handling for invalid credentials
- ✅ Loading states
- ✅ Mobile responsive design

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Update `.env` with your Supabase project details:
   ```env
   VITE_SUPABASE_URL=your-supabase-project-url
   VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Supabase Setup

To use this authentication system, you'll need a Supabase project with:

1. A Supabase project created at [supabase.com](https://supabase.com)
2. Authentication enabled (it's enabled by default)
3. Your project URL and anonymous key added to `.env`

## Project Structure

```
src/
  ├── components/
  │   ├── LoginForm.jsx     # Login form component
  │   ├── LoginForm.css     # Login form styles
  │   ├── Dashboard.jsx     # Authenticated user dashboard
  │   └── Dashboard.css     # Dashboard styles
  ├── contexts/
  │   └── AuthContext.jsx   # Authentication context and hooks
  ├── lib/
  │   └── supabase.js      # Supabase client configuration
  ├── App.jsx              # Main app component
  └── main.jsx            # App entry point
```

## Authentication Flow

1. **Login**: Users enter email/password, handled by `LoginForm`
2. **Session Management**: Handled automatically by `AuthContext`
3. **Protected Routes**: Dashboard only shows when authenticated
4. **Logout**: Clears session and returns to login form
