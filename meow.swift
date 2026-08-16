#!/usr/bin/env swift
//
//  MEOW Engine — Swift version
//  Transpiled from Python, runs gladiators via subprocess
//

import Foundation

struct Gladiator: Codable {
    let language: String
    let cmd: [String]
    let disciplines: [String]
    let arenas: [String]
    let root: String
}

struct ArenaPolicy: Codable {
    let name: String
    let validators: Int
    let consensus: String
    let adversarial: Bool
    let scoring: String
}

struct GladiatorResult: Codable {
    let gladiator: String
    let arena: String
    let ok: Bool
    let output: String
    let score: Double?
}

struct TournamentResult: Codable {
    let cat: String
    let results: [GladiatorResult]
}

func loadPolicy(name: String) throws -> ArenaPolicy {
    let arenasDir = URL(fileURLWithPath: #file).deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("arenas")
    let defaultData = try Data(contentsOf: arenasDir.appendingPathComponent("default.yaml"))
    let defaultDict = try YAMLDecoder().decode([String: Any].self, from: defaultData)
    
    var policyDict = defaultDict
    let specificURL = arenasDir.appendingPathComponent("\(name).yaml")
    if FileManager.default.fileExists(atPath: specificURL.path) {
        let specificData = try Data(contentsOf: specificURL)
        let specificDict = try YAMLDecoder().decode([String: Any].self, from: specificData)
        policyDict.merge(specificDict) { _, new in new }
    }
    
    return ArenaPolicy(
        name: name,
        validators: policyDict["validators"] as? Int ?? 3,
        consensus: policyDict["consensus"] as? String ?? "majority",
        adversarial: policyDict["adversarial"] as? Bool ?? false,
        scoring: policyDict["scoring"] as? String ?? "accuracy"
    )
}

func discoverGladiators(languagesDir: String) -> [Gladiator] {
    let base = URL(fileURLWithPath: languagesDir)
    let enumerator = FileManager.default.enumerator(at: base, includingPropertiesForKeys: [.isDirectoryKey])!
    
    var gladiators: [Gladiator] = []
    
    for case let fileURL as URL in enumerator {
        if fileURL.lastPathComponent == "contract.json" {
            let data = try! Data(contentsOf: fileURL)
            let contract = try! JSONDecoder().decode(Contract.self, from: data)
            
            let root = fileURL.deletingLastPathComponent()
            var cmd = contract.runtime.cmd
            cmd = cmd.map { $0.replacingOccurrences(of: "{root}", with: root.path) }
            
            let gladiator = Gladiator(
                language: contract.language,
                cmd: cmd,
                disciplines: contract.disciplines,
                arenas: contract.arenas,
                root: root.path
            )
            gladiators.append(gladiator)
        }
    }
    
    return gladiators.sorted { $0.language < $1.language }
}

struct Contract: Codable {
    let language: String
    let runtime: Runtime
    let disciplines: [String]
    let arenas: [String]
}

struct Runtime: Codable {
    let cmd: [String]
    let native: Bool
}

func runArena(arena: String, gladiators: [Gladiator]) -> [GladiatorResult] {
    let policy = try! loadPolicy(name: arena)
    let convoked = gladiators.filter { $0.disciplines.contains("construct") && $0.arenas.contains(arena) }
    
    var results: [GladiatorResult] = []
    
    for gladiator in convoked {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = gladiator.cmd
        
        let inputPipe = Pipe()
        let outputPipe = Pipe()
        process.standardInput = inputPipe
        process.standardOutput = outputPipe
        
        let request = ["discipline": "construct", "arena": arena]
        let inputData = try! JSONEncoder().encode(request)
        
        try! process.run()
        inputPipe.fileHandleForWriting.write(inputData)
        inputPipe.fileHandleForWriting.closeFile()
        
        let outputData = outputPipe.fileHandleForReading.readDataToEndOfFile()
        process.waitUntilExit()
        
        let output = String(data: outputData, encoding: .utf8) ?? ""
        let result = try! JSONDecoder().decode(GladiatorResult.self, from: outputData)
        
        results.append(GladiatorResult(
            gladiator: gladiator.language,
            arena: arena,
            ok: result.ok,
            output: result.output,
            score: result.score
        ))
    }
    
    return results
}

func runTournament() -> TournamentResult {
    let gladiators = discoverGladiators(languagesDir: "../languages")
    let arenas = ["ears", "cheeks", "padding", "whiskers", "eyes", "mouth", "nose", "geometry", "head_top"]
    
    var allResults: [GladiatorResult] = []
    
    for arena in arenas {
        let results = runArena(arena: arena, gladiators: gladiators)
        allResults.append(contentsOf: results)
    }
    
    // Build cat ASCII
    let cat = """
          |\\      _,,,---,,_
     ZZZzz /,`.-'`'    -.  ;-;;,_
        |,4-  ) )-,_. ,\\ (  `'-'
       '---''(_/--'  `-'\\_)
    """
    
    return TournamentResult(cat: cat, results: allResults)
}

@main
struct MEOW {
    static func main() {
        let args = CommandLine.arguments
        
        if args.contains("--list-gladiators") {
            let gladiators = discoverGladiators(languagesDir: "../languages")
            for g in gladiators {
                print("\(g.language.padding(toLength: 12, withPad: " ", startingAt: 0)) \(g.disciplines.joined(separator: ",").padding(toLength: 24, withPad: " ", startingAt: 0)) \(g.arenas.joined(separator: ","))")
            }
            exit(0)
        }
        
        if let idx = args.firstIndex(of: "--arena"), idx + 1 < args.count {
            let arena = args[idx + 1]
            let gladiators = discoverGladiators(languagesDir: "../languages")
            let results = runArena(arena: arena, gladiators: gladiators)
            let encoder = JSONEncoder()
            encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
            let data = try! JSONEncoder().encode(results)
            print(String(data: data, encoding: .utf8)!)
            exit(0)
        }
        
        if args.contains("--tournament") {
            let result = runTournament()
            print(result.cat)
            print("🏆 Tournament complete!")
            exit(0)
        }
        
        if args.contains("--judge") {
            let result = runTournament()
            // Print mutations
            exit(0)
        }
        
        if args.contains("--caesar") {
            print("Et tu, Brute?")
            exit(0)
        }
        
        print("Usage: meow --list-gladiators | --arena NAME | --tournament | --judge | --caesar")
        exit(1)
    }
}

// Simple YAML decoder for policy files
struct YAMLDecoder {
    func decode(_ type: [String: Any].Type, from data: Data) throws -> [String: Any] {
        let string = String(data: data, encoding: .utf8)!
        var result: [String: Any] = [:]
        
        for line in string.split(separator: "\n") {
            let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)
            if trimmed.isEmpty || trimmed.hasPrefix("#") { continue }
            if let colonIndex = trimmed.firstIndex(of: ":") {
                let key = String(trimmed[..<colonIndex]).trimmingCharacters(in: .whitespaces)
                let value = String(trimmed[trimmed.index(after: colonIndex)...]).trimmingCharacters(in: .whitespaces)
                
                if let intVal = Int(value) {
                    result[key] = intVal
                } else if let boolVal = Bool(value) {
                    result[key] = boolVal
                } else {
                    result[key] = value
                }
            }
        }
        return result
    }
}

extension Bool {
    init?(_ string: String) {
        if string == "true" { self = true }
        else if string == "false" { self = false }
        else { return nil }
    }
}