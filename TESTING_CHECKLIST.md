# HomeBuddy UI Testing Checklist

## Pre-Testing Setup

- [ ] Run `npm install` to ensure all dependencies are installed
- [ ] Start the development server: `npm run dev`
- [ ] Open browser to the local URL (usually http://localhost:5173)
- [ ] Open browser developer console (F12) to monitor for errors

---

## 1. Authentication Tests

### Login Screen
- [ ] **Visual Check**: Login screen displays correctly
  - [ ] HomeBuddy logo and branding visible
  - [ ] Email input field present
  - [ ] Password input field present
  - [ ] "Sign In" button visible
  - [ ] "Sign up" link present

- [ ] **Functionality**:
  - [ ] Enter email: `test@example.com`
  - [ ] Enter password: `password123`
  - [ ] Click "Sign In"
  - [ ] Success toast notification appears
  - [ ] Redirected to chat screen
  - [ ] Username displayed correctly

### Signup Screen
- [ ] Click "Sign up" from login screen
- [ ] **Visual Check**: Signup screen displays correctly
  - [ ] "Create Account" title visible
  - [ ] Name, Email, Password fields present
  - [ ] "Create Account" button visible
  - [ ] "Sign in" link present

- [ ] **Functionality**:
  - [ ] Enter name: `John Doe`
  - [ ] Enter email: `john@example.com`
  - [ ] Enter password: `test123`
  - [ ] Click "Create Account"
  - [ ] Success toast notification appears
  - [ ] Redirected to chat screen
  - [ ] Username "John Doe" displayed

### Logout
- [ ] From chat screen, click "Logout" button
- [ ] Logout toast notification appears
- [ ] Redirected back to login screen

---

## 2. Chat Interface Tests

### Initial Load
- [ ] Welcome message displays correctly
- [ ] Lists all four input methods (Voice, QR, Photo, Text)
- [ ] Features list is visible
- [ ] Input area is visible at bottom
- [ ] All four input method buttons are visible

### UI Layout
- [ ] **Header**:
  - [ ] HomeBuddy logo and title visible
  - [ ] "Smart Appliance Assistant" subtitle
  - [ ] "My Appliances" button visible
  - [ ] Logout button visible

- [ ] **Main Chat Area**:
  - [ ] Messages display correctly
  - [ ] User messages aligned right (purple background)
  - [ ] Assistant messages aligned left (white background)
  - [ ] Avatars display for both user and assistant
  - [ ] Timestamps visible on messages
  - [ ] Scrolling works properly

- [ ] **Input Panel**:
  - [ ] Three buttons visible: Voice Input, Scan QR, Upload Photo
  - [ ] Textarea for text input visible
  - [ ] Send button visible (purple gradient)
  - [ ] Placeholder text: "Type your message or use one of the input methods above..."

- [ ] **Right Sidebar**:
  - [ ] Quick Stats section visible
  - [ ] Available Features section visible
  - [ ] Stats cards display correctly

---

## 3. Text Input Tests

- [ ] Click in the textarea
- [ ] Type: "How do I fix my washing machine?"
- [ ] Press Enter
- [ ] Message appears in chat (right side, purple)
- [ ] Loading indicator appears briefly
- [ ] AI response appears (left side, white)
- [ ] Auto-scroll to bottom works

- [ ] **Multi-line Test**:
  - [ ] Type some text
  - [ ] Press Shift+Enter
  - [ ] New line created (message not sent)
  - [ ] Press Enter
  - [ ] Message sends

- [ ] **Empty Message Test**:
  - [ ] Try to send empty message
  - [ ] Send button should be disabled
  - [ ] No message sent

---

## 4. Voice Input Tests

⚠️ **Note**: Requires Chrome/Edge browser and microphone permissions

- [ ] Click "Voice Input" button
- [ ] Browser requests microphone permission (if first time)
- [ ] Grant permission
- [ ] Button turns red
- [ ] Icon changes to MicOff
- [ ] Toast: "Listening... Speak now" appears
- [ ] Speak clearly: "What's wrong with my dishwasher?"
- [ ] Button returns to normal
- [ ] Text appears in textarea
- [ ] Toast: "Speech captured!" appears
- [ ] Review text and click Send
- [ ] Message sends normally

### Error Cases
- [ ] Click "Voice Input" again during recording
- [ ] Recording stops
- [ ] Button returns to normal
- [ ] Try in Firefox (should show error: "not supported")

---

## 5. QR Scanner Tests

⚠️ **Note**: Requires camera permissions

### Opening Scanner
- [ ] Click "Scan QR" button
- [ ] Browser requests camera permission (if first time)
- [ ] Grant permission
- [ ] Modal overlay appears
- [ ] "Scan QR Code" title visible
- [ ] Camera preview shows
- [ ] Close button (X) visible in top-right

### Scanning
- [ ] Prepare a QR code (can use online QR generator)
- [ ] Position QR code in camera view
- [ ] QR code is detected and highlighted
- [ ] Modal closes automatically
- [ ] User message appears: "Scanned QR code for [device]"
- [ ] Assistant response includes device information
- [ ] Device context loaded (shows in chat)

### Cancel Scanning
- [ ] Click "Scan QR" button
- [ ] Click X button (close)
- [ ] Modal closes
- [ ] No message sent
- [ ] Camera stops

---

## 6. Photo Upload Tests

### Uploading Photo
- [ ] Click "Upload Photo" button
- [ ] File picker opens
- [ ] Select an image file (JPG, PNG, etc.)
- [ ] Click "Open"
- [ ] Loading state appears
- [ ] User message appears: "📷 Uploaded image: [filename]"
- [ ] Processing toast notification appears
- [ ] Assistant response about the image
- [ ] Can ask follow-up questions about the image

### Multiple Uploads
- [ ] Upload first photo
- [ ] Wait for processing
- [ ] Upload second photo
- [ ] Both images are referenced in conversation

### Invalid File
- [ ] Click "Upload Photo"
- [ ] Try to select a non-image file (e.g., .txt)
- [ ] Error toast: "Please upload an image file"
- [ ] No message sent

---

## 7. Advanced Features Tests

### Appliance Manager
- [ ] Click "My Appliances" button
- [ ] Right sidebar changes to Appliance Manager
- [ ] Can add new appliance (if backend is running)
- [ ] Can view appliance list
- [ ] Can close sidebar with X button

### Device Context
- [ ] Scan a device QR code (or manually set device)
- [ ] Ask: "How do I clean this?"
- [ ] Response should be device-specific
- [ ] Device info visible somewhere in UI

### Safety Warnings
- [ ] Ask a safety-related question (e.g., "Can I touch the heating element?")
- [ ] Check if safety warning appears
- [ ] Error toast for dangerous actions
- [ ] Safety flag in message metadata

---

## 8. Responsive Design Tests

### Desktop (> 1200px)
- [ ] Full layout with sidebar
- [ ] All buttons visible
- [ ] Chat area is wide
- [ ] Sidebar shows Quick Stats

### Tablet (768px - 1200px)
- [ ] Resize browser window to ~900px
- [ ] Layout adjusts properly
- [ ] Buttons remain accessible
- [ ] Text remains readable

### Mobile (< 768px)
- [ ] Resize browser window to ~400px
- [ ] Input panel stacks vertically
- [ ] Buttons are touch-friendly
- [ ] Chat messages adjust width
- [ ] Sidebar becomes full-screen overlay

---

## 9. Error Handling Tests

### Backend Offline
- [ ] Ensure backend server is NOT running
- [ ] Try to send a message
- [ ] Error message appears
- [ ] Toast notification about backend connection
- [ ] App doesn't crash

### Permission Denied
- [ ] Block microphone in browser settings
- [ ] Click "Voice Input"
- [ ] Error message about permissions
- [ ] Instructions to enable

- [ ] Block camera in browser settings
- [ ] Click "Scan QR"
- [ ] Error message about camera access
- [ ] Instructions to enable

### Network Issues
- [ ] Disable internet (or use browser dev tools to simulate offline)
- [ ] Try various actions
- [ ] Appropriate error messages display
- [ ] App remains functional

---

## 10. Performance Tests

### Load Time
- [ ] Clear browser cache
- [ ] Reload page
- [ ] Note load time (should be < 3 seconds)
- [ ] All assets load correctly

### Message Rendering
- [ ] Send 20+ messages rapidly
- [ ] Check if UI remains responsive
- [ ] Scrolling is smooth
- [ ] No memory leaks (check dev tools)

### Large Images
- [ ] Upload a large image (5MB+)
- [ ] Check upload progress
- [ ] Verify processing completes
- [ ] No timeout errors

---

## 11. Browser Compatibility

### Chrome/Edge
- [ ] All features work
- [ ] Voice input works
- [ ] QR scanner works
- [ ] UI renders correctly

### Firefox
- [ ] Basic features work
- [ ] Voice input shows appropriate error
- [ ] QR scanner works
- [ ] UI renders correctly

### Safari
- [ ] Basic features work
- [ ] Voice input works (with webkit prefix)
- [ ] QR scanner works
- [ ] UI renders correctly

---

## 12. Accessibility Tests

- [ ] Tab through all interactive elements
- [ ] Focus indicators visible
- [ ] Can operate with keyboard only
- [ ] Screen reader announces elements correctly
- [ ] Color contrast is sufficient
- [ ] Text is readable (not too small)

---

## Test Results Summary

**Date Tested**: _________________  
**Browser**: _________________  
**Screen Size**: _________________  

**Overall Status**:
- [ ] ✅ All tests passed
- [ ] ⚠️ Minor issues (list below)
- [ ] ❌ Major issues (list below)

**Issues Found**:
1. _________________________________________________
2. _________________________________________________
3. _________________________________________________

**Notes**:
_________________________________________________________
_________________________________________________________
_________________________________________________________

---

## Quick Smoke Test (5 minutes)

If you're short on time, run these critical tests:

1. [ ] Login works
2. [ ] Can send text message
3. [ ] Voice input button responds
4. [ ] QR scanner opens
5. [ ] Photo upload dialog opens
6. [ ] Logout works
7. [ ] No console errors

---

**Last Updated**: January 25, 2026  
**Version**: 1.0
