# 🐾 Animal Classifier AI

An intelligent web application that uses deep learning to classify animal images. Built with TensorFlow, Flask, and modern web technologies.

## 🚀 Features

- **10 Animal Classes**: Cat, Dog, Horse, Sheep, Cow, Elephant, Butterfly, Chicken, Spider, Squirrel
- **Transfer Learning**: Uses MobileNetV2 pre-trained on ImageNet
- **Modern UI**: Beautiful, responsive design with drag-and-drop support
- **Real-time Predictions**: Fast inference with confidence scores
- **Cloud Deployment**: Ready for deployment on Render

## 🛠️ Technologies Used

- **Backend**: Flask, TensorFlow/Keras, Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **ML Model**: MobileNetV2 (Transfer Learning)
- **Deployment**: Render

## 📦 Installation

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AI_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 🌐 Deployment on Render

### Prerequisites
- GitHub account
- Render account (free tier available)
- Model file (`animals10_model.keras`) in your repository

### Steps:

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Create a new Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `animal-classifier` (or your choice)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
     - **Instance Type**: Free tier

3. **Environment Variables** (Optional):
   - `DEBUG`: `false`
   - `PORT`: Auto-set by Render

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

### Important Notes for Render:

- **Model File Size**: Ensure `animals10_model.keras` is included in your repo
- **Cold Starts**: Free tier apps sleep after inactivity; first request may take 30-60 seconds
- **Memory Limits**: Free tier has 512MB RAM; optimize model if needed
- **Build Time**: Initial build takes longer due to TensorFlow installation

## 📁 Project Structure

```
AI_project/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── runtime.txt            # Python version
├── animals10_model.keras  # Trained ML model
├── static/
│   ├── style.css         # Styles
│   └── script.js         # Frontend logic
├── templates/
│   └── index.html        # Main page
└── Animals-10.ipynb      # Training notebook
```

## 🧠 Model Information

- **Architecture**: MobileNetV2 (Transfer Learning)
- **Input Size**: 224x224 RGB images
- **Training Dataset**: Animals-10 from Kaggle
- **Training Accuracy**: ~90%+
- **Inference Time**: <1 second per image

## 🎯 Usage

1. Open the web application
2. Click or drag-and-drop an animal image
3. Click "Predict Animal"
4. View the prediction and confidence score

## 🔧 Troubleshooting

### Model Not Loading
- Ensure `animals10_model.keras` exists in the root directory
- Check model compatibility with TensorFlow version

### Deployment Issues on Render
- Verify all files are pushed to GitHub
- Check build logs for errors
- Ensure requirements.txt has correct dependencies

### Slow Predictions
- Free tier has limited resources
- Consider upgrading to paid tier for better performance

## 📊 API Endpoints

### `GET /`
Returns the main web interface

### `POST /predict`
Predicts animal from uploaded image
- **Input**: Form data with `file` field
- **Output**: JSON with `prediction` and `confidence`

### `GET /health`
Health check endpoint
- **Output**: JSON with service status

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ for machine learning enthusiasts

## 🙏 Acknowledgments

- TensorFlow team for amazing ML framework
- Kaggle for the Animals-10 dataset
- MobileNet architecture creators

---

**Note**: This is an educational project. For production use, consider adding:
- User authentication
- Rate limiting
- Model versioning
- Comprehensive error handling
- Analytics and monitoring
