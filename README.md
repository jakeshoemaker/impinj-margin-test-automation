# impinj-margin-test-automation
A automation tool for performing margin tests on RFID tags using a Impinj RFID reader

#### You will need a conda env with the following python libraries
- pandas
- numpy
- send2trash

#### The following dotnet package will be required from nuGet: 
- Impinj.Octane.Sdk


## How to use: 
#### assuming you have a RFID reader connected to your local machine type:
`dotnet build`  to build the C# dll's

then it is as simple as running the following command in a ps shell in the project directory:
`./marginTest.ps1`

## NOTE inside the marginTest.ps1 file the user will have to edit the batch script to activate the specific conda env. 
## the user also must have Conda Scripts added to PATH.
