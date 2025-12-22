
param(
    [string]$ProcessPath
)

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Get-UIHierarchy {
    param($element, $indent)
    
    try {
        $automationElement = [System.Windows.Automation.AutomationElement]$element
        if ($null -eq $automationElement) { return }

        $name = $automationElement.Current.Name
        $controlType = $automationElement.Current.ControlType.ProgrammaticName
        $isEnabled = $automationElement.Current.IsEnabled

        # Output basic JSON-like structure
        Write-Output "{ ""title"": ""$name"", ""control_type"": ""$controlType"", ""enabled"": $isEnabled }"

        $children = $automationElement.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
        foreach ($child in $children) {
            Get-UIHierarchy -element $child -indent ($indent + 1)
        }
    } catch {
        # Ignore access errors
    }
}

if ($ProcessPath -ne $null -and $ProcessPath -ne "") {
    # Launch process
    $process = Start-Process -FilePath $ProcessPath -PassThru
    Start-Sleep -Seconds 3
    
    # Try to find the window handle
    # This is a simplification; robust logic needs to find the window by PID
    try {
        $root = [System.Windows.Automation.AutomationElement]::FromHandle($process.MainWindowHandle)
        if ($root) {
            Write-Output "["
            Get-UIHierarchy -element $root -indent 0
            Write-Output "]"
        }
    } catch {
        Write-Error "Could not attach to window."
    }
}
