# Homebuddy - React Frontend Architecture

## Component Structure

```
src/app/
├── App.tsx                    # Main application component
├── components/
│   ├── ApplianceManager.tsx   # Appliance list & details
│   ├── RepairHistory.tsx      # Repair logging & history
│   ├── Chat.tsx               # Main chat interface
│   ├── Login.tsx              # Authentication
│   ├── Signup.tsx             # User registration
│   └── ui/                    # UI components (50+)
│       ├── button.tsx
│       ├── card.tsx
│       ├── dialog.tsx
│       └── ... (shadcn components)
└── styles/
    ├── index.css              # Main styles
    ├── tailwind.css           # Tailwind configuration
    └── theme.css              # Theme variables
```

## Key Components

### ApplianceManager
- Manages appliance list display
- Shows appliance status badges
- Displays maintenance tasks
- Handles appliance CRUD operations

### RepairHistory
- Repair logging form
- Repair history list
- Statistics dashboard
- Pattern detection display

### Chat
- Main interface
- Conversation display
- Message input
- Settings access

## Styling

- **Tailwind CSS v4** for utility-first styling
- **CSS custom properties** for theming
- **Responsive design** for all screen sizes
- **Dark mode support** for better accessibility

## Development

```bash
npm install --legacy-peer-deps
npm run dev        # Development server
npm run build      # Production build
npm run preview    # Preview build
```

## Frontend Technologies

✅ React 18.3.1 (latest)
✅ TypeScript 5+ (strict mode)
✅ Tailwind CSS v4 (utility-first)
✅ Vite 6.3.5 (fast bundler)
✅ lucide-react (icons)
✅ sonner (notifications)

---

**Frontend Lead: Hetvi2211**
