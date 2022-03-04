param (
    [Parameter()]
    $process
)

jupyter nbconvert --to html $process --output-dir ..\mjsmagalhaes.github.io\content\notebook