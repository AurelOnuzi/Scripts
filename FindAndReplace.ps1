###Aurel Onuzi


#user input handling
Param (
    [String]$userfile = $( Read-Host -Prompt "Enter a filename or foldername to analyze: ") ,
	[String]$userreplace = $( Read-Host -Prompt "Enter a find and replace CSV file: " ),
	[String]$userpref = $( Read-Host -Prompt "Do you want to overwrite the file (enter 0) or save in a new location(enter 1): " )
)
#import the csv file
$ReplacementList = Import-Csv $userreplace -Header ("FindWord","ReplaceWord");
if ( $userpref -eq '0' ) {
	#overwriting the file with the new replaced one, checking to see if its a text file
	if ( $userfile.Extension -eq 'txt' ){
		Get-Content -Force -Path $userfile |
		ForEach-Object {
			#runs through the file and replaces the data in the file with the replaceword
			$Content = Get-Content -Force -Path $_.FullName;
			foreach ($word in $ReplacementList)
			{
				$Content = $Content.Replace($word.FindWord, $word.ReplaceWord)
			}
			#updates content saving it with the same filename
			Set-Content -Force -Path $_.FullName -Value $Content
		}
	}
	
	else{
		#similar to other, but -Recurse added for directories with files/directories in them
		Get-ChildItem $userfile -Recurse -Force |
		ForEach-Object {
			$Content = Get-Content -Force -Path $_.FullName;
			foreach ($word in $ReplacementList)
			{
				$Content = $Content.Replace($word.FindWord, $word.ReplaceWord)
			}
			Set-Content -Force -Path $_.FullName -Value $Content
			}
		}
}
else{
	$newloc = $(Read-Host -Prompt "Enter a file location to place the modified file(s): ")
	
	if ( $userfile.Extension -eq 'txt' ){
		#creates copy to the new file location
		Get-Content -Force -Path $userfile |
		Copy-Item -Destination $newloc -Recurse -Container -Force

		Get-ChildItem -Force -Path $newloc |
		ForEach-Object {
			$Content = Get-Content -Force -Path $_.FullName;
			foreach ($word in $ReplacementList){
				if(-not $?){
					continue
				}
				$Content = $Content.Replace($word.FindWord, $word.ReplaceWord)
			}
			Set-Content -Force -Path $_.FullName -Value $Content
			}
	}
	else{	
		Get-ChildItem $userfile |
		Copy-Item -Destination $newloc -Recurse -Container -Force
		
		Get-ChildItem $newloc -Recurse -Force  | 
		ForEach-Object {
			$Content = Get-Content -Force -Path $_.FullName;
			foreach ($word in $ReplacementList){
				if(-not $?){
					continue
				}
				$Content = $Content.Replace($word.FindWord, $word.ReplaceWord)
			}
			Set-Content -Force -Path $_.FullName -Value $Content
			}
	}
}