# TypeScribe v1.0

Need to send out a hundred organic Christmas cards? Or you have a fifty page essay due and _Brush Script_ doesn't quite cut it?
Got you covered.

**TypeScribe** is a tool that uses Machine Learning to convert typed text into realistic handwriting by introducing customizable degrees of randomness and variations, to make it all so believable.

<table align="center">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/077894b9-6fb9-430e-8b13-de8ae40866e0" alt="" width="300"></td>
    <td><img src="https://github.com/user-attachments/assets/cf977b24-a56a-4f0c-aa15-da991e487b0b" alt="" width="300"></td>
    <td><img src="https://github.com/user-attachments/assets/7804ff31-4403-4621-90ac-3b65b0aac13f" alt="" width="300"></td>
    <td><img src="https://github.com/user-attachments/assets/defd2a1c-d28b-49fa-bb49-20f297a830c1" alt="" width="300"></td>
  </tr>
      <tr>
    <td>TypeScribe</td>
    <td>Totally not homework</td>
    <td>A truly heartfelt letter</td>
    <td>Christmas Cards too!?</td>
  </tr>
</table>

### Features
- **Realistic Handwriting Generation with a Recurrent Neural Network (RNN)**
- **Choose from 12 predefined handwriting styles.**
- **Adjust line spacing, page size, margins, ink color, pen thickness, and more.**
- **User-friendly interface**
- **Automatically splits large texts into multiple lines, paragraphs and pages.**
- **Scalable SVG Output that maintains quality even on resizing**


### Getting Started

There are two ways to get things rolling:

1. **Download the Executable:**
   - Head to the [Releases page](https://github.com/rudyoactiv/typescribe-handwriting/releases) and download the **TypeScribe-v1.0.zip** package.
   - Unzip the file and double-click **TypeScribe.exe** to launch the application.

2. **Clone the Repository:**
   - Alternatively, you can clone this repo using ```git clone https://github.com/rudyoactiv/typescribe-handwriting.git```
   - Navigate to the cloned directory.
   - With Anaconda installed, run ```conda env create -f environment.yml``` to create an environment.
   - Run ```conda activate test_hand``` to activate your environment.
   - Run the program with ```python gui.py```


### Usage
1. Launch the application with the command ```python gui.py``` or double click TypeScribe.exe.
2. Enter your text and adjust settings via the interface.
3. Preview the layout and handwriting style.
4. Click **Generate**.
5. Select a destination folder for your files.
6. Wait while it generates your output. May take a minute.

### Known Issues
- Antivirus programs may flag (and even delete) the executable. This is due to the way Python programs are built and handled by Windows and cannot possibly be fixed. However, there is no cause for concern.
- The application itself may freeze while your file is being generated. No need to panic, it does not crash.

### Future Plans
- A more responsive design
- More customization options
- Increasing the valid character set
- Fix antivirus false positives
- Build an installer to replace the zip
- Extra text formatting options (vary alignment, ink colors in a single document).

### Acknowledgements
This project is inspired by the work in the [handwriting-synthesis](https://github.com/sjvasquez/handwriting-synthesis) repository by **sjvasquez**, which provides the foundational implementation for handwriting synthesis using Recurrent Neural Networks (RNNs). 

The handwriting synthesis in TypeScribe is based on the work presented in the paper **[Generating Sequences with Recurrent Neural Networks](https://arxiv.org/abs/1308.0850)** by Alex Graves. [Graves, A. (2013). *Generating sequences with recurrent neural networks*. arXiv preprint arXiv:1308.0850.]

---

Thank you for trying TypeScribe! ✍️
