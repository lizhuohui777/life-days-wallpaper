import AppKit
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 3024, pixelsHigh: 1964, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
NSColor(calibratedRed: 0.28, green: 0.39, blue: 0.45, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: 3024, height: 1964).fill()
for (i, color) in [NSColor(calibratedRed: 0.23, green: 0.33, blue: 0.35, alpha: 1), NSColor(calibratedRed: 0.18, green: 0.28, blue: 0.29, alpha: 1)].enumerated() {
    color.setFill()
    let hill = NSBezierPath()
    hill.move(to: NSPoint(x: 0, y: 0)); hill.line(to: NSPoint(x: 0, y: 650 - i * 150))
    hill.curve(to: NSPoint(x: 3024, y: 550 - i * 150), controlPoint1: NSPoint(x: 800, y: 900 - i * 200), controlPoint2: NSPoint(x: 1900, y: 200 + i * 100))
    hill.line(to: NSPoint(x: 3024, y: 0)); hill.close(); hill.fill()
}
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.95])!.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
