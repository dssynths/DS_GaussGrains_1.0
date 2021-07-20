
import tensorflow as tf
import os
import argparse
import glob

# Read and print data:

def get_arguments():

    parser = argparse.ArgumentParser(description="myParser")
    parser.add_argument("--filename", required=False)
    parser.add_argument("--fileDir", required=False)
    return parser.parse_args()

def main():

    # folderConsistency()

    args = get_arguments()
    
    if args.filename != None:
        filename = [args.filename] # here, the result is the file name, e.g. config or config-special
        printRecord(filename)

    elif args.fileDir != None:

        path = os.path.abspath(args.fileDir)
    
        if os.path.isdir(path):
    
            files = []
            for file in os.listdir(path):
                if file.endswith(".tfrecord"):
                    printRecord(os.path.join(path, file))
        else:
            print("Provide correct directory name")
    else:
        print("Provide arguments")

def printRecord(filename):

    raw_dataset = tf.data.TFRecordDataset(filename)
    
    for raw_record in raw_dataset.take(1):
      tfToJSon = tf.train.Example()
      tfToJSon.ParseFromString(raw_record.numpy())
      print(tfToJSon)


if __name__ == '__main__':
    main()