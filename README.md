
### This is codebase aimed to write automatic python script that reads some valid JEE Rolenumbers from a file with their DOB and using OCR fill alpha numeric captch code and enter into systemto find candidate details

The directory structure is as follows:-
```
.
|-- README.md
|-- appliedStudentsList.csv
|-- WorkingOnCaptchasForJEEResults.py
|-- imagesForGit/ 
|-- data/
|     |-- captcha.png
|     |-- results.csv
```

### To run the project use simple command
```
	$ python3 WorkingOnCaptchasForJEEResults.py appliedStudentsList.csv
```

### Snippets to get enthu
1. Input Data in form of csv having student's JEE Roll Number and Date Of Birth 
![Input Data in a csv having student's JEE Roll Number and Date Of Birth](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/inputCSV.png)

2. Filling internal details along with Captcha cracking using OCR and Selenium 
![craking Fig 1](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/crackingCaptchEx1.jpg) 
![craking Fig 2](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/crackingCaptchEx2.jpg)

2.1 A cracked Captcha		![captch1](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/634NL4.png)

Predicted alphaNumeric = "634NL4"

<br /> 

2.2 Another Cracked Captcha 	![captcha2](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/BV8948.png)

Predicted alphaNumeric = "BV8948"

<br /> 

3. Capturing Internal Deatils<br /> 
![internalDeatils](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/internalDeatilsCaptured.jpg)

4. Process followed per candidate<br /> 
![processFollowed](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/processFollowed.jpg)

5. Final JEE Results obtained snippet<br /> 
![finalResults](https://github.com/lihkinVerma/alphaNumericCaptchaCrack/blob/master/imagesForGit/resultCSV.png)

 
Deatiled discussion can be found at https://medium.com/@lih.verma/cracking-alpha-numeric-captcha-via-image-processing-and-ocr-make-life-easier-and-automatic-d89fe7becd36

