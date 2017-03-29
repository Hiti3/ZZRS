import java.lang.Integer;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.io.PrintWriter;
import java.text.DecimalFormat;

public class Main {
    
    private static final String inputFile = "input.txt";
    private static final String outputFile = "output.txt";
    private static final String resultsFile = "results.txt";
    private static final int iterations = 20;
    
    private static Data[] elements;
    private static long[] times;
    
    public static void main (String[] args) throws Exception
    {
        elements = new Data[Integer.parseInt(args[0])];
        times = new long[iterations];
        
        long startTime;
        long stopTime;
        for (int i = 0; i < iterations; i++) {
            startTime = System.nanoTime();
            
            readFile(inputFile);
            sortData();
            writeFile(outputFile);
            
            stopTime = System.nanoTime();
            times[i] = stopTime - startTime;
        }
        writeResultsFile(resultsFile);
    }
    
    private static void readFile(String path) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader(new File(path)));
        
        String line;
        int i = 0;
        while ((line = br.readLine()) != null) {
            Data element = new Data();
            element.setValue(Integer.parseInt(line));
            elements[i] = element;
            i++;
        }
    }
    
    private static void writeFile(String path) throws Exception {
        PrintWriter writer = new PrintWriter(path, "UTF-8");
        for (int i = 0; i < elements.length; i++) {
            writer.println(Integer.toString(elements[i].getValue()));
        }
        writer.close();
    }
    
    private static void writeResultsFile(String path) throws Exception {
        PrintWriter writer = new PrintWriter(path, "UTF-8");
        long avgTime = 0;
        for (int i = 0; i < times.length; i++) {
            writer.println("Čas: " + new DecimalFormat("#.###").format(((double) times[i]) / 1000000) + " ms");
            avgTime += times[i];
        }
        avgTime = avgTime / iterations;
        writer.println("Povprečni čas: " + new DecimalFormat("#.###").format(((double) avgTime) / 1000000) + " ms");
        writer.close();
    }
    
    private static void sortData() {
        Data temp = null;
        for (int i = 0; i < elements.length; i++) {
            for (int j = 1; j < (elements.length - i); j++) {
                
                if (elements[j - 1].isBigger(elements[j])) {
                    temp = elements[j - 1];
                    elements[j - 1] = elements[j];
                    elements[j] = temp;
                }
            }
        }
    }
}