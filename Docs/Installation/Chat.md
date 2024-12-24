
### Installation SoftwareAI
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
![UI](Docs/Installation/imgChat/Screenshot_1.png)
- **2 - Enter the key name and there is openai key**  
![UI](Docs/Installation/imgChat/Screenshot_2.png)
- **3 - Click Create Key**  
![UI](Docs/Installation/imgChat/Screenshot_3.png)
### **Configuring Keys Firebase**
- **1 - Add any name to your Firebase app**  
![UI](Docs/Installation/imgChat/Screenshot_4.png)
- **1 - Add realtime database url**  
![UI](Docs/Installation/imgChat/Screenshot_5.png)
- **1.1 - you can find its url by accessing the databaserealtime section**  
![UI](Docs/Installation/imgChat/Screenshot_6.png)
- **2 - Add realtime storage url**  
![UI](Docs/Installation/imgChat/Screenshot_7.png)
- **2.1 - you can find its url by accessing the storage section**  
![UI](Docs/Installation/imgChat/Screenshot_8.png)
- **3 - Add your downloaded firebase credentials**  
![UI](Docs/Installation/imgChat/Screenshot_9.png)
- **3.1 - Navigate to where the credentials are and click open**  
![UI](Docs/Installation/imgChat/Screenshot_10.png)
- **3.2 - Click to Create key**  
![UI](Docs/Installation/imgChat/Screenshot_11.png)
- **3.3 - Step by step to find generate firebase keys**  
![UI](Docs/Installation/imgChat/Screenshot_16.png)
![UI](Docs/Installation/imgChat/Screenshot_17.png)
![UI](Docs/Installation/imgChat/Screenshot_18.png)
![UI](Docs/Installation/imgChat/Screenshot_19.png)
- **After completing all the steps to add openai keys and firebase keys**  
- **You are ready to start the chat**  
 
### Start chat using a small script
```python
from softwareai.Chat import initchat
initchat()
```
