

import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the pre-trained model
@st.cache_resource
def load_trained_model():
    model = load_model("plant_leaf_diseases_model.h5")
    return model

# Disease information dictionary
disease_info = {
    
    "Pepper__bell___Bacterial_spot": {
        "Prevention": "🌱 **Prevention**: Use copper-based fungicides to prevent bacterial infection and spread. Remove infected leaves immediately to limit contamination. Rotate crops yearly to avoid soilborne bacteria buildup.",
        "Chemicals": "🧪 **Chemicals**: Copper oxychloride, Streptomycin, and other copper-based fungicides. Always follow the manufacturer's instructions regarding application.",
        "Watering": "💧 **Watering**: Avoid overhead irrigation to prevent water droplets spreading the bacteria. Water at the base of plants using a drip system or soaker hoses.",
        "Additional Care": "🛠️ **Additional Care**: Ensure proper air circulation around plants by spacing them adequately. Prune any excess foliage and avoid watering in the evening to reduce the risk of fungal and bacterial infections overnight."
    },
    "Pepper__bell___healthy": {
        "Prevention": "🌱 **Prevention**: Maintain healthy soil with proper nutrients and pH levels. Provide sufficient sunlight (at least 6-8 hours per day) to enhance plant immunity. Apply organic matter or compost to the soil to improve its health.",
        "Chemicals": "🧪 **Chemicals**: None needed for healthy plants. Organic treatments, such as neem oil or insecticidal soap, can be used preventively to control pests.",
        "Watering": "💧 **Watering**: Water regularly, ensuring that the soil is moist but not soggy. Allow the top 1-2 inches of soil to dry out before watering again to prevent root rot.",
        "Additional Care": "🛠️ **Additional Care**: Ensure proper drainage to prevent waterlogging. Use organic fertilizers rich in potassium and phosphorus to promote strong root and fruit development."
    },
    "Potato___Early_blight": {
        "Prevention": "🌱 **Prevention**: Remove infected leaves immediately and dispose of them properly to prevent the spread of spores. Use resistant potato varieties if available. Plant in well-drained, moderately fertile soil to reduce disease risk.",
        "Chemicals": "🧪 **Chemicals**: Chlorothalonil, Mancozeb, and other fungicides labeled for early blight control. Always read and follow the manufacturer's instructions for use and application frequency.",
        "Watering": "💧 **Watering**: Water early in the day to ensure that leaves dry out before evening, which reduces the chance of fungal infections. Avoid watering overhead; water at the base of the plant.",
        "Additional Care": "🛠️ **Additional Care**: Practice crop rotation to reduce soilborne diseases and improve soil health. Remove plant debris at the end of the growing season to reduce overwintering pathogen populations."
    },
    "Potato___healthy": {
        "Prevention": "🌱 **Prevention**: Ensure balanced soil nutrition and avoid over-fertilizing with nitrogen, as this can make plants more susceptible to disease. Maintain proper crop rotation to reduce pest and disease buildup in the soil.",
        "Chemicals": "🧪 **Chemicals**: None needed for healthy plants. Regular application of organic fertilizers or compost will provide the necessary nutrients.",
        "Watering": "💧 **Watering**: Water consistently but ensure good drainage to avoid waterlogging, which can promote diseases like blight. Use drip irrigation to direct water at the base of the plant and minimize wetting the foliage.",
        "Additional Care": "🛠️ **Additional Care**: Maintain weed control to reduce competition for nutrients. Prune dead or yellowing leaves to reduce the risk of fungal infection."
    },
       "Tomato_Bacterial_spot": {
        "Prevention": "🌱 **Prevention**: Avoid working in the garden when plants are wet to minimize bacterial spread. Apply resistant cultivars when possible. Practice crop rotation and destroy infected plants.",
        "Chemicals": "🧪 **Chemicals**: Copper hydroxide, Oxytetracycline, and other bactericides effective against bacterial spot. Always apply when conditions are conducive to disease spread.",
        "Watering": "💧 **Watering**: Water at the base of the plant using drip irrigation to prevent water droplets from spreading bacteria. Keep foliage dry.",
        "Additional Care": "🛠️ **Additional Care**: Remove and destroy infected plant material to reduce the spread of bacteria. Use good spacing between plants to improve airflow and reduce moisture buildup around the leaves."
    },
    "Tomato_Early_blight": {
        "Prevention": "🌱 **Prevention**: Remove infected leaves promptly and practice crop rotation to prevent the buildup of pathogens in the soil. Plant resistant varieties if available.",
        "Chemicals": "🧪 **Chemicals**: Chlorothalonil, Mancozeb, and other fungicides effective against early blight. Apply preventively during wet conditions or as soon as the first signs of disease appear.",
        "Watering": "💧 **Watering**: Water early in the day to allow leaves to dry before evening, reducing the risk of fungal growth. Avoid watering overhead.",
        "Additional Care": "🛠️ **Additional Care**: Maintain proper spacing between plants and avoid dense planting to improve air circulation. Remove plant debris at the end of the growing season to reduce overwintering pathogens."
    },
    "Tomato_Late_blight": {
        "Prevention": "🌱 **Prevention**: Provide adequate spacing between plants for better air circulation. Remove infected plants and all plant debris. Practice crop rotation to reduce soilborne pathogens.",
        "Chemicals": "🧪 **Chemicals**: Mancozeb, Metalaxyl, and other fungicides effective against late blight. Apply fungicides when conditions are favorable for blight, such as cool and moist weather.",
        "Watering": "💧 **Watering**: Water early in the day to ensure that foliage dries before nightfall. Avoid overhead watering, which can encourage fungal growth.",
        "Additional Care": "🛠️ **Additional Care**: Use resistant tomato varieties and keep plants spaced properly to reduce the spread of the disease. Prune affected leaves and dispose of them in sealed bags to prevent the spread of spores."
    },
    "Tomato_Leaf_Mold": {
        "Prevention": "🌱 **Prevention**: Prune dense foliage to increase air circulation around the plants and reduce humidity. Remove infected leaves to prevent mold spread.",
        "Chemicals": "🧪 **Chemicals**: Fungicides like chlorothalonil and mancozeb can be used to control leaf mold. Always follow the manufacturer’s guidelines regarding frequency and application.",
        "Watering": "💧 **Watering**: Water early in the day, ensuring foliage is dry by evening. Water at the base of plants to avoid wetting the leaves.",
        "Additional Care": "🛠️ **Additional Care**: Ensure good plant spacing to reduce overcrowding, and avoid conditions of high humidity. Implement proper drainage to reduce waterlogging around plant roots."
    },
    "Tomato_Septoria_leaf_spot": {
        "Prevention": "🌱 **Prevention**: Remove infected leaves and apply fungicides to prevent further spread. Avoid overhead watering to keep foliage dry.",
        "Chemicals": "🧪 **Chemicals**: Chlorothalonil, Mancozeb, and other fungicides effective against Septoria leaf spot. Apply fungicides on a regular schedule during the growing season.",
        "Watering": "💧 **Watering**: Water at the base of the plant, keeping the leaves dry to reduce the spread of the disease.",
        "Additional Care": "🛠️ **Additional Care**: Ensure good air circulation around plants and prune any dead or diseased material to prevent infection from spreading. Practice crop rotation and remove infected debris."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "Prevention": "🌱 **Prevention**: Maintain healthy plant growth and keep plants well-watered to reduce stress. Avoid over-fertilizing, which can make plants more susceptible to pests.",
        "Chemicals": "🧪 **Chemicals**: Acaricides such as abamectin or neem oil can be used to control spider mites. Always follow the manufacturer's instructions when applying pesticides.",
        "Watering": "💧 **Watering**: Water regularly but avoid overwatering, as waterlogged soil can lead to root rot. Ensure consistent moisture to help plants resist pest stress.",
        "Additional Care": "🛠️ **Additional Care**: Introduce natural predators like ladybugs or predatory mites to control spider mites. Remove heavily infested leaves and dispose of them to reduce pest populations."
    },
    "Tomato_Target_Spot": {
        "Prevention": "🌱 **Prevention**: Use resistant varieties of tomatoes and avoid excessive watering, which can promote fungal growth. Prune affected leaves and destroy them to reduce infection spread.",
        "Chemicals": "🧪 **Chemicals**: Chlorothalonil, Mancozeb, and other fungicides can be applied to control target spot. Apply fungicide preventively when conditions are conducive to disease spread.",
        "Watering": "💧 **Watering**: Water early in the morning to allow the plant to dry before nightfall. Avoid watering foliage to keep leaves dry and minimize disease spread.",
        "Additional Care": "🛠️ **Additional Care**: Maintain good airflow around plants by ensuring adequate spacing between them. Prune infected foliage and remove plant debris to minimize the spread of spores."
    },
    "Tomato_Tomato_YellowLeaf_Curl_Virus": {
        "Prevention": "🌱 **Prevention**: Control aphid populations to prevent virus spread. Remove and destroy infected plants immediately. Consider planting resistant varieties if available.",
        "Chemicals": "🧪 **Chemicals**: Use insecticides like imidacloprid to control aphids and prevent further viral spread. Apply as soon as aphids are detected.",
        "Watering": "💧 **Watering**: Water at the base of the plant and avoid getting water on the foliage to prevent spreading the virus via contaminated water droplets.",
        "Additional Care": "🛠️ **Additional Care**: Practice good pest management, monitor for aphid infestations, and apply insecticides as necessary. Use sticky traps to monitor aphid populations."
    },
    "Tomato_Tomato_mosaic_virus": {
        "Prevention": "🌱 **Prevention**: Remove infected plants and control aphids.",
        "Chemicals": "🧪 **Chemicals**: Insecticides to control aphids.",
        "Watering": "💧 **Watering**: Water at the base of plants, ensuring leaves stay dry.",
        "Additional Care": "🛠️ **Additional Care**: Use resistant tomato varieties and practice good pest management."
    },
    "Tomato_healthy": {
        "Prevention": "🌱 **Prevention**: Ensure consistent watering and remove dead plant material.",
        "Chemicals": "🧪 **Chemicals**: None needed for healthy plants.",
        "Watering": "💧 **Watering**: Water deeply but allow the soil to dry between waterings.",
        "Additional Care": "🛠️ **Additional Care**: Fertilize every 2-3 weeks with a balanced fertilizer."
    }
}

    # Add similar styling for other diseases

# Prediction function
def predict_plant_leaf_disease(uploaded_image, model, target_size=(256, 256)):
    # Preprocess the image
    img = uploaded_image.resize(target_size)
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction, axis=1)[0]

    # Replace this with your actual class labels
    class_labels = [
        "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy", "Potato___Early_blight", 
        "Potato___Late_blight", "Potato___healthy", "Tomato_Bacterial_spot", "Tomato_Early_blight",
        "Tomato_Late_blight", "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two_spotted_spider_mite", 
        "Tomato__Target_Spot", "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus", "Tomato_healthy"
    ]
    predicted_class_label = class_labels[predicted_class_index]
    confidence_score = prediction[0][predicted_class_index]

    return predicted_class_label, confidence_score

# Streamlit app interface
def main():
    st.title("🌿 Plant Leaf Disease Detection")
    st.markdown("""
        Upload a leaf image to detect its disease and receive detailed care instructions.  
        This tool uses a deep learning model to analyze plant health and provide actionable insights.  
    """)

    # Load the model
    model = load_trained_model()

    # File uploader
    uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Display uploaded image
        uploaded_image = Image.open(uploaded_file)
        # Display uploaded image
        st.image(uploaded_image, caption="📸 Uploaded Image", use_container_width=True)
        # Predict disease
        with st.spinner("🔍 Analyzing the image..."):
            predicted_class, confidence = predict_plant_leaf_disease(uploaded_image, model)
        
        # Display prediction
        st.success("✅ Prediction Complete!")
        st.markdown(f"### 🏷️ **Predicted Class:** `{predicted_class}`")
        st.markdown(f"### 📊 **Confidence Score:** `{confidence:.2f}`")

        # Display disease information
        if predicted_class in disease_info:
            st.subheader("🩺 Disease Information and Care")
            st.markdown(disease_info[predicted_class]["Prevention"])
            st.markdown(disease_info[predicted_class]["Chemicals"])
            st.markdown(disease_info[predicted_class]["Watering"])
            st.markdown(disease_info[predicted_class]["Additional Care"])
        else:
            st.warning("⚠️ No additional information available for this disease.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
