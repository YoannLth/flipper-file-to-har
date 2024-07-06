# Flipper to HAR Converter

This script converts Flipper files (.flipper) to HAR files (.har). It allows you to extract network request data from Flipper and save it in the HAR format for further analysis. Made with the help of Chat-GPT 😎

## Requirements

- Python 3.9.12
- Flipper 0.177.0

## Installation

1. Clone or download this repository to your local machine.

## Usage

### Export a Flipper file
1. Open Flipper.

2. Connect your device and ensure it is selected in the Flipper toolbar.

3. Navigate to the "Network" section in Flipper.

4. Perform the desired actions or interactions in your app to generate network requests.

5. Flipper will capture and display the network requests in the "Network" panel.

6. Click on the settings icon in the bottom left of the window

7. Choose the "Export Flipper file" and choose a desired location

8. Click save and make sure "Network" checkbox is checked

9. Click "Ok"

### Command-line Usage

To convert a Flipper file to HAR using the command-line interface:
1. Navigate to project directory

2. Run `python flipper_to_har.py <input_file_path> <output_file_path>`

### Quick Actions (macOS)

Quick Actions provide a convenient way to convert Flipper files to HAR through the macOS Finder.

To set up a Quick Action using AppleScript:

1. Copy the file "flipper_to_har.py" and save in "~/scripts/". Otherwise, you could have an "[Errno 1] Operation not permitted" error

2. Open Automator on your Mac.

3. Create a new Quick Action workflow.

4. Add the "Run AppleScript" action to the workflow.

5. Change the Workflow configuration by changing "Workflow receives current Automatic (nothing)" with "Workflow receives files or folders"

6. Replace the default AppleScript with the following code:

   ```applescript
   on run {input, parameters}
       set inputFile to POSIX path of item 1 of input
       set filePath to POSIX path of input
       set scriptPath to "/path/to/flipper_to_har.py"
       
       set folderPath to (do shell script "dirname " & quoted form of inputFile)
       set outputFilePath to folderPath & "/output.har"

       set command to "/opt/homebrew/bin/python3 " & quoted form of scriptPath & " " & quoted form of inputFile & " " & quoted form of outputFilePath

       do shell script command
       
       return input
   end run
   ````
Replace /path/to/flipper_to_har.py with the path to the script file.

7. Save the Quick Action workflow with an appropriate name (e.g., "Convert Flipper to HAR").

#### Use Quick Actions on a file
To convert a Flipper file to HAR using the Quick Action:

1. Right-click on the Flipper file in the Finder.

2. Navigate to the "Quick Actions" submenu.

3. Select the "Convert Flipper to HAR" action.

The Flipper file will be converted to HAR, and the resulting file will be saved in the same folder as the input file with the name "output.har".

### Open a HAR file
You can then open the HAR file using Charles Proxy or a Browser. Make sure to erase sensitive informations before sharing the HAR file.




