
### 📚 Chat Installation documentation

### **Installation SoftwareAI**  
```bash
pip install --upgrade SoftwareAI
```
### **Editor**  
```python
from softwareai.Editor import initeditor
initeditor()
```
### **Configuring Keys openai** 
- **1 - Click on the key icon in the menu**  
![UI](imgChat/Screenshot_1.png)
- **2 - Enter the key name and there is openai key**  
![UI](imgChat/Screenshot_2.png)
- **3 - Click Create Key**  
![UI](imgChat/Screenshot_3.png)
### **Configuring Keys Firebase**
- **1 - Add any name to your Firebase app**  
![UI](imgChat/Screenshot_4.png)
- **1 - Add realtime database url**  
![UI](imgChat/Screenshot_5.png)
- **1.1 - you can find its url by accessing the databaserealtime section**  
![UI](imgChat/Screenshot_6.png)
- **2 - Add realtime storage url**  
![UI](imgChat/Screenshot_7.png)
- **2.1 - you can find its url by accessing the storage section**  
![UI](imgChat/Screenshot_8.png)
- **3 - Add your downloaded firebase credentials**  
![UI](imgChat/Screenshot_9.png)
- **3.1 - Navigate to where the credentials are and click open**  
![UI](imgChat/Screenshot_10.png)
- **3.2 - Click to Create key**  
![UI](imgChat/Screenshot_11.png)
- **3.3 - Step by step to find generate firebase keys**  
![UI](imgChat/Screenshot_16.png)
![UI](imgChat/Screenshot_17.png)
![UI](imgChat/Screenshot_18.png)
![UI](imgChat/Screenshot_19.png)
- **After completing all the steps to add openai keys and firebase keys**  
- **You are ready to start the chat**  
 
### Start chat using a small script
```python
from softwareai.Chat import initchat
initchat()
```
