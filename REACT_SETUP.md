# CompanionAI - React UI Setup Guide

## 🎉 Migration Complete!

Your CompanionAI application has been successfully migrated from Streamlit to React!

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)
Simply run the batch file:
```batch
start_companion_ai.bat
```

This will:
1. Install Python dependencies
2. Install Node.js dependencies
3. Start the FastAPI backend on port 8000
4. Start the React frontend on port 5173

### Option 2: Manual Start

#### Terminal 1 - Backend API
```batch
uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2 - React Frontend
```batch
npm run dev
```

## 📱 Access Points

- **React Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## ✨ What's Changed

### Before (Streamlit)
- Simple Python-based UI
- Limited customization
- Port 8502

### After (React)
- Modern, responsive React UI
- Rich component library (Radix UI, shadcn/ui)
- Better user experience
- Port 5173 (Vite dev server)

## 🎨 Key Features of the React UI

1. **Modern Chat Interface**
   - Real-time messaging with the AI backend
   - Safety warnings displayed prominently
   - Source citations for answers
   - Processing time metrics

2. **Multiple Input Methods**
   - Text input
   - Voice recognition (Web Speech API)
   - Image upload
   - QR code scanning

3. **Safety Features**
   - Visual alerts for dangerous situations
   - Safety level indicators
   - Color-coded warnings

4. **Responsive Design**
   - Works on desktop and mobile
   - Tailwind CSS styling
   - Smooth animations

## 🔧 Configuration

The React app connects to the backend using the environment variable:
```
VITE_BACKEND_URL=http://127.0.0.1:8000
```

You can change this in the `.env` file.

## 🐳 Docker Deployment

The Docker configuration has been updated for React:

```batch
docker-compose up --build
```

This will:
- Build the React app
- Serve it with Nginx on port 80
- Run the FastAPI backend
- Configure proxy for API calls

Access the app at: http://localhost

## 📦 Dependencies

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Radix UI components
- shadcn/ui
- Lucide icons

### Backend
- FastAPI
- Python 3.8+
- (Existing Python dependencies)

## 🛠️ Development

### Installing Dependencies
```batch
npm install
```

### Running in Development Mode
```batch
npm run dev
```

### Building for Production
```batch
npm run build
```

The built files will be in the `dist/` folder.

## 📝 API Integration

The React app communicates with the backend through the API service located at:
`src/services/api.ts`

Key endpoints used:
- `POST /answer` - Get AI responses
- `POST /upload` - Upload images
- `GET /health` - Check backend status
- `GET /metrics` - Get performance metrics

## 🎯 Next Steps

1. **Test the Application**: Run the startup script and test all features
2. **Customize Styling**: Edit Tailwind configuration or component styles
3. **Add Features**: Extend the Chat component or add new components
4. **Deploy**: Use the Docker setup for production deployment

## 🐛 Troubleshooting

### Backend not connecting
- Ensure the backend is running on port 8000
- Check the `VITE_BACKEND_URL` in `.env`
- Look for CORS errors in browser console

### npm install fails
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again

### Port already in use
- Change the port in `vite.config.ts`
- Or kill the process using the port

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

---

**Happy Coding! 🎉**
