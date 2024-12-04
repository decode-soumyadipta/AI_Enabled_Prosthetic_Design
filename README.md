
# 🦾 AI-Enabled Prosthetic Design Using Openvino Software Toolkit
# (🤖optimizing unet-camvid model)

Welcome to the **AI-Enabled Prosthetic Design** project, where advanced AI technologies meet human-centric design! This platform leverages CT scan data and machine learning to create and customize prosthetic limbs, aiming to revolutionize prosthetics for better fit, functionality, and accessibility.

---

## 🌟 Features
- **CT Scan-Based Prosthetic Design**: Upload CT scans of the opposite healthy limb or residual limb for precise design.
- **Mirror Imaging Algorithms**: Automatically create a mirrored model of the healthy limb for symmetry.
- **Population-Based Prosthetic Models**: Use pre-trained databases to generate prosthetics for congenital conditions.
- **Customizable Prosthetics**: Tailor the prosthetic design to user needs (e.g., lightweight, athletic, robotic-assisted).
- **3D Printing Ready**: Export prosthetic designs as STL files for easy 3D printing.

---

## 🛠️ Tech Stack
**Backend**:  
- **Flask**: Lightweight Python framework for API and server-side logic.  
- **Intel OpenVINO Toolkit**: Accelerate AI-based image processing and prediction tasks.  
- **Pandas/Numpy**: Data handling for CT scan metadata.  

**Frontend**:  
- **React**: Dynamic, component-based UI for user interaction.  
- **Bootstrap/Material UI**: Modern styling for responsive designs.  

**AI/ML Models**:  
- **Intel Distribution of OpenVINO** for model optimization and inference.  
- Pre-trained models from **TensorFlow** or **PyTorch** for segmentation and design generation.  

**Database**:  
- **SQLite**: Lightweight database for user data and prosthetic designs.

---

## 📂 File Structure

### **Backend**
```plaintext
backend/
├── app/
│   ├── static/             # Static assets for the Flask backend
│   │   ├── css/
│   │   │   └── style.css   # Styling for result pages
│   │   ├── js/
│   │   │   └── app.js      # JavaScript for interactivity
│   │   └── images/         # Placeholder for assets
│   ├── templates/          # HTML templates rendered by Flask
│   │   ├── index.html      # Home page template
│   │   ├── upload.html     # Prosthetic upload page
│   │   └── result.html     # Results display page
│   ├── routes/             # API endpoints and Flask routing logic
│   │   ├── __init__.py
│   │   ├── api.py          # API for ML processing
│   │   └── prosthetic_routes.py  # Routes for prosthetic generation
│   ├── models/             # Models for handling data and AI
│   │   ├── __init__.py
│   │   └── prosthetic_model.py  # ML models for CT processing
│   ├── utils/              # Helper functions
│   │   ├── file_processing.py  # CT scan file handling
│   │   └── image_preprocessing.py  # Image pre-processing for ML
│   ├── tests/              # Unit tests
│   │   ├── test_routes.py
│   │   └── test_models.py
│   └── app.py              # Main Flask app
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

### **Frontend**
```plaintext
frontend/
├── public/
│   ├── index.html          # Base HTML for React
│   └── favicon.ico         # Favicon for the app
├── src/
│   ├── components/         # Reusable components
│   │   ├── Header.js       # Header component
│   │   ├── Footer.js       # Footer component
│   │   ├── ProstheticUpload.js # Upload form
│   │   └── ResultDisplay.js    # Display prosthetic results
│   ├── pages/              # Main pages
│   │   ├── Home.js         # Homepage
│   │   ├── Upload.js       # Upload CT scan page
│   │   └── Results.js      # Results and download page
│   ├── App.js              # Main React app
│   ├── index.js            # Entry point for React
│   └── App.css             # Styling for the React app
├── package.json            # React dependencies
└── README.md               # Frontend documentation
```

### **Docs**
```plaintext
docs/
└── *                      # Documentation, API references, and user guides
```

---

## 🚀 How It Works
1. **Upload**: The user uploads a CT scan of their opposite limb (or residual limb).  
2. **Processing**: The backend processes the scan:
   - Performs image segmentation.
   - Creates a mirrored design or selects a reference from a database.  
3. **Custom Design**: The user can customize the prosthetic's appearance and functionality.  
4. **Download**: Export the final design as an STL file for 3D printing.

---

## 🧰 Using Intel Toolkits
- **Intel OpenVINO Toolkit**:
  - Use for pre-trained segmentation models and faster inference.
  - Install it with:
    ```bash
    pip install openvino-dev
    ```
  - Example:
    ```python
    from openvino.inference_engine import IECore
    ie = IECore()
    model = ie.read_network(model='segmentation_model.xml', weights='segmentation_model.bin')
    ```
- **Intel Distribution of Python**:
  - Optimized for handling CT scan data and training ML models.

---

## 🗂️ Steps to Get Started
### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/AI-Enabled-Prosthetic-Design.git
   ```
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### **Run the Project**
1. Start the Flask backend:
   ```bash
   python backend/app.py
   ```
2. Start the React frontend:
   ```bash
   npm start
   ```

### **Test the Application**
- Run unit tests:
  ```bash
  pytest backend/tests
  ```

---

## 🔄 System Flow
1. **User Interaction**:  
   - Upload CT scans.  
   - Customize prosthetic design.  
2. **Backend Processing**:  
   - Segmentation of scans using Intel AI models.  
   - Design generation with mirroring or database references.  
3. **Frontend Display**:  
   - Preview prosthetic designs.  
   - Download STL files.

---

## 🧩 Key Focus Areas
- Accurate CT scan preprocessing and segmentation.  
- User-friendly customization tools.  
- Scalable architecture to integrate future AI models.

---

## 👨‍💻 Development Tools
- Use **Visual Studio Code** for lightweight and modular development.  
- Use **Intel OpenVINO Model Optimizer** for pre-trained model optimization.

---

