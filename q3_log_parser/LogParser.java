package q3_log_parser;
import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * LogParser - Parses a log file and returns the most recent N log lines
 * matching the given log types (error, warning, info, debug).
 *
 * Usage: java LogParser <filePath> [numLines] [types]
 * Example: java LogParser app.log 10 info,debug
 */
public class LogParser {

    // All valid log types the user can filter by
    private static final Set<String> VALID_TYPES =
        new HashSet<>(Arrays.asList("error", "warning", "info", "debug"));

    /**
     * Main parsing method.
     * Reads the file from the bottom up and collects lines matching the requested types.
     *
     * @param filePath  Path to the log file
     * @param numLines  How many matching lines to return (most recent)
     * @param types     Comma-separated log types e.g. "error,info"
     * @return          List of matching log lines (in chronological order)
     */
    public static List<String> parseLogs(String filePath, int numLines, String types)
            throws Exception {

        // --- Validate file path ---
        File file = new File(filePath);
        if (!file.exists() || !file.isFile()) {
            throw new Exception("ERROR: Invalid file path -> " + filePath);
        }

        // --- Validate and collect log types ---
        Set<String> requestedTypes = new HashSet<>();
        for (String t : types.split(",")) {
            String trimmed = t.trim().toLowerCase();
            if (!VALID_TYPES.contains(trimmed)) {
                throw new Exception("ERROR: Invalid log type -> '" + trimmed +
                    "'. Valid types are: error, warning, info, debug");
            }
            requestedTypes.add(trimmed);
        }

        // --- Read all lines from file ---
        List<String> allLines = Files.readAllLines(file.toPath());

        // --- Scan from BOTTOM to TOP (most recent logs are at the end) ---
        List<String> result = new ArrayList<>();
        for (int i = allLines.size() - 1; i >= 0 && result.size() < numLines; i--) {
            String line = allLines.get(i).trim();

            // The log format is [INFO], [DEBUG], [ERROR], [WARNING]
            // Extract the type inside the brackets
            if (line.startsWith("[")) {
                int closingBracket = line.indexOf("]");
                if (closingBracket > 0) {
                    // Get the word inside [ ] and lowercase it
                    String logType = line.substring(1, closingBracket).toLowerCase();
                    if (requestedTypes.contains(logType)) {
                        result.add(line); // collect this matching line
                    }
                }
            }
        }

        // Reverse so output is shown oldest → newest (natural reading order)
        Collections.reverse(result);
        return result;
    }

    /**
     * Entry point. Accepts command line arguments.
     * Arg 1: file path (required)
     * Arg 2: number of lines (optional, default = 10)
     * Arg 3: log types comma separated (optional, default = "error")
     */
    public static void main(String[] args) {
        try {
            // Default values as per assignment
            String filePath = "";
            int numLines = 10;
            String types = "error";

            // Read arguments if provided
            if (args.length >= 1) filePath = args[0];
            if (args.length >= 2) numLines = Integer.parseInt(args[1]);
            if (args.length >= 3) types = args[2];

            // Must provide file path
            if (filePath.isEmpty()) {
                throw new Exception("ERROR: File path is required as first argument.");
            }

            System.out.println("=== Log Parser ===");
            System.out.println("File   : " + filePath);
            System.out.println("Lines  : " + numLines);
            System.out.println("Types  : " + types);
            System.out.println("==================");

            // Run the parser
            List<String> logs = parseLogs(filePath, numLines, types);

            if (logs.isEmpty()) {
                System.out.println("No matching log entries found.");
            } else {
                System.out.println("Found " + logs.size() + " matching log(s):\n");
                for (String log : logs) {
                    System.out.println(log);
                }
            }

        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
    }
}