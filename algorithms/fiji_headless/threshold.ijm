// Fiji ImageJ Macro for Headless Threshold Segmentation
// Parse command line arguments in key=value format
args = getArgument();
print("Arguments received: " + args);

// Initialize variables
inputFolder = "";
outputFolder = "";
thresholdMode = "above";
minThreshold = 128;
maxThreshold = 255;

// Parse key=value pairs
parts = split(args, " ");
for (i = 0; i < parts.length; i++) {
    if (indexOf(parts[i], "folder=") >= 0) {
        inputFolder = substring(parts[i], indexOf(parts[i], "=") + 1);
    }
    if (indexOf(parts[i], "output=") >= 0) {
        outputFolder = substring(parts[i], indexOf(parts[i], "=") + 1);
    }
    if (indexOf(parts[i], "mode=") >= 0) {
        thresholdMode = substring(parts[i], indexOf(parts[i], "=") + 1);
    }
    if (indexOf(parts[i], "min_threshold=") >= 0) {
        minThreshold = parseInt(substring(parts[i], indexOf(parts[i], "=") + 1));
    }
    if (indexOf(parts[i], "max_threshold=") >= 0) {
        maxThreshold = parseInt(substring(parts[i], indexOf(parts[i], "=") + 1));
    }
}

// Set default output folder if not provided
if (outputFolder == "") {
    outputFolder = "/bilayers/output_images";
    print("No output folder specified, using default: " + outputFolder);
}

print("Input folder: " + inputFolder);
print("Output folder: " + outputFolder);
print("Threshold mode: " + thresholdMode);
print("Min threshold: " + minThreshold);
print("Max threshold: " + maxThreshold);

// Get list of files in input folder
fileList = getFileList(inputFolder);

// Process each image
for (i = 0; i < fileList.length; i++) {
    fileName = fileList[i];

    // Check if file is an image (skip directories)
    if (endsWith(fileName, ".tif") || endsWith(fileName, ".tiff") ||
        endsWith(fileName, ".png") || endsWith(fileName, ".jpg") ||
        endsWith(fileName, ".jpeg")) {

        // Skip already processed files
        if (indexOf(fileName, "_threshold") >= 0) {
            continue;
        }

        inputPath = inputFolder + "/" + fileName;
        print("Processing: " + inputPath);
        print("Opening image...");

        // For OME-TIFF files with incomplete metadata, copy to temp file without .ome extension
        // This forces Fiji to use the regular TIFF reader instead of Bio-Formats
        actualPath = inputPath;
        if (endsWith(fileName, ".ome.tif") || endsWith(fileName, ".ome.tiff")) {
            tempPath = "/tmp/" + replace(fileName, ".ome.", ".");
            print("Copying to temp file to bypass OME metadata: " + tempPath);
            File.copy(inputPath, tempPath);
            actualPath = tempPath;
        }

        open(actualPath);
        print("Image opened successfully");

        // Get the image title for saving later
        imageTitle = getTitle();
        baseName = substring(imageTitle, 0, lastIndexOf(imageTitle, "."));
        print("Image title: " + imageTitle);

        // Apply threshold based on mode
        print("Applying threshold mode: " + thresholdMode);
        setOption("BlackBackground", true);

        if (thresholdMode == "above") {
            print("Thresholding above: " + minThreshold);
            setThreshold(minThreshold, 255);
            run("Convert to Mask");
        } else if (thresholdMode == "below") {
            print("Thresholding below: " + minThreshold);
            setThreshold(0, minThreshold);
            run("Convert to Mask");
        } else if (thresholdMode == "between") {
            print("Thresholding between: " + minThreshold + " and " + maxThreshold);
            setThreshold(minThreshold, maxThreshold);
            run("Convert to Mask");
        } else {
            print("Unknown threshold mode: " + thresholdMode + ", using default (above)");
            setThreshold(minThreshold, 255);
            run("Convert to Mask");
        }

        print("Mask created");

        // Create output directory if it doesn't exist
        File.makeDirectory(outputFolder);

        // Save the result
        outputPath = outputFolder + "/" + baseName + "_threshold.tif";
        print("Saving to: " + outputPath);
        saveAs("Tiff", outputPath);
        print("Saved: " + outputPath);

        // Clean up
        close();
        print("Closed image");
    }
}

print("Threshold segmentation completed successfully");
print("Processed folder: " + inputFolder);
print("Output folder: " + outputFolder);
print("Threshold mode: " + thresholdMode);
print("Min threshold: " + minThreshold);
print("Max threshold: " + maxThreshold);
