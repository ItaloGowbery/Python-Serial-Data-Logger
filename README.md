# Python Serial Data Logger with Graphical Interface

This is a Python project with a graphical user interface (GUI) that reads data from a serial port and displays it in real time in a table and a graph. The application also saves the collected data to an XLSX file.

The code has been configured to receive a fixed number of values per reading.

---

### Features

* **Graphical User Interface (GUI):** Allows you to easily select the serial port and start/stop reading data.
* **Port Detection:** The software automatically lists the serial ports available on your system.
* **Real-time Monitoring:** Displays the received data in a table and a dynamic graph.
* **Configurable Delay:** Allows you to adjust the time (in seconds) between each data log entry (to work properly, the microcontroller must send data every 1 second).
* **Save Data:** Collected data can be saved to an Excel (.xlsx) file after reading.

---

### Interface

![Alternative text](interface.png)

---

### Requirements

To run the application, you need the following Python libraries:

* **pyserial:** For communication with the serial port.
* **ttkbootstrap:** For the modern graphical interface style (an extension of Tkinter).
* **matplotlib:** For plotting graphs.
* **pandas:** For data manipulation and saving in Excel format.
* **openpyxl:** To allow pandas to save .xlsx files.

You can install them with the following command:

```bash
pip install pyserial ttkbootstrap matplotlib pandas openpyxl
```

### Data Format

The program expects to receive a string with **8 integer values**, separated by commas, terminated by a newline character (`\n`).

**Example:**
`value1,value2,value3,value4,value5,value6,value7,value8`

---

### How to Adapt to Your Needs

To use the code with a different number of data points or with specific names for each value, you will need to edit the `main.py` file.

1.  **Adjust the Number of Values:** In the `read_serial()` function, modify the line `if len(valores) == 8:` to the number of values you are sending.
2.  **Adjust Names and Columns:** In the `stop_and_save()` function and in other parts of the code, edit the `colunas` and `nomes` lists to match your data.

---

### How to Use

1.  Clone the repository.
2.  Install the necessary libraries.
3.  Connect your device (Arduino, ESP32, etc.) to the computer.
4.  Run the script:
   
    ```bash
    python main.py
    ```
6.  Select the correct serial port from the list and click **"Start"**.
7.  To stop reading and save the data, click **"Stop and Save"**.
