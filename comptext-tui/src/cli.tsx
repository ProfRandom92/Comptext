import React, { useState, useEffect } from "react";
import { render, Text, Box, useInput, useApp } from "ink";
import { exec } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

// Get repo root relative to this file's compiled location (dist/cli.js)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, "../..");

interface CommandOption {
  key: string;
  name: string;
  command: string;
}

const COMMANDS: CommandOption[] = [
  { key: "s", name: "Status Screen", command: "python -m modules.cli.cli_entrypoint status --dry-run" },
  { key: "d", name: "Doctor Diagnostics", command: "python -m modules.cli.cli_entrypoint doctor --dry-run" },
  { key: "v", name: "Local Verify Screen", command: "python -m modules.cli.cli_entrypoint verify --dry-run" },
  { key: "w", name: "Workspace Validation", command: "python -m modules.cli.cli_entrypoint validate workspace --dry-run" },
  { key: "e", name: "Evidence Verify (Sample)", command: "python -m modules.cli.cli_entrypoint evidence verify --sample" },
];

function App() {
  const { exit } = useApp();
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [output, setOutput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [exitCode, setExitCode] = useState<number | null>(null);

  useInput((input) => {
    const key = input.toLowerCase();
    if (key === "q") {
      exit();
      return;
    }

    const matched = COMMANDS.find((cmd) => cmd.key === key);
    if (matched) {
      setSelectedKey(matched.key);
      setLoading(true);
      setOutput("Running backend command...");
      setExitCode(null);

      exec(matched.command, { cwd: REPO_ROOT }, (error, stdout, stderr) => {
        setLoading(false);
        if (error) {
          setExitCode(error.code || 1);
          setOutput(stdout + "\n" + stderr + "\n" + error.message);
        } else {
          setExitCode(0);
          setOutput(stdout);
        }
      });
    }
  });

  return (
    <Box flexDirection="column" padding={1} borderStyle="round" borderColor="cyan">
      <Box marginBottom={1}>
        <Text color="yellow" bold>
          COMPTEXT TUI WORKBENCH (Node/Ink Layer)
        </Text>
      </Box>

      <Box flexDirection="column" marginBottom={1}>
        <Text color="gray">Press a key to run a backend verification command:</Text>
        {COMMANDS.map((cmd) => (
          <Text key={cmd.key}>
            <Text color="green" bold>[{cmd.key.toUpperCase()}]</Text> {cmd.name}
          </Text>
        ))}
        <Text color="red" bold>[Q] Quit</Text>
      </Box>

      {selectedKey && (
        <Box flexDirection="column" borderStyle="single" borderColor="magenta" padding={1}>
          <Text bold>
            Active:{" "}
            <Text color="cyan">
              {COMMANDS.find((cmd) => cmd.key === selectedKey)?.command}
            </Text>
          </Text>
          <Box marginTop={1} flexDirection="column">
            {loading ? (
              <Text color="yellow">Executing Python Backend...</Text>
            ) : (
              <>
                <Text color="gray">--- Output ---</Text>
                <Text>{output}</Text>
                <Text color="gray">--------------</Text>
                <Text>
                  Exit Code:{" "}
                  <Text color={exitCode === 0 ? "green" : "red"}>
                    {exitCode}
                  </Text>
                </Text>
              </>
            )}
          </Box>
        </Box>
      )}
    </Box>
  );
}

render(<App />);
