function myFunction()
{
    var lst = document.querySelector('#list')
    var selectedtools = [].filter.call(lst.options, option => option.selected).map(option => option.text);
    console.log(selectedtools)
    var dockerfile = "FROM ubuntu:18.04\nRUN apt-get update && apt-get install -y \\\n\t"

    for(var tool in selectedtools){
        dockerfile += selectedtools[tool] + " \\ \n\t"
    }

    dockerfile += "&& rm -rf /var/lib/apt/lists/*"

    document.getElementById('dockerfile').value = dockerfile
    alert(document.getElementById('dockerfile').value)
}










// var form = document.getElementById('myForm')

// form.addEventListener('submit',function(event){
//     event.preventDefault()

//     var lst = document.querySelector('#list')
//     var selectedtools = [].filter.call(lst.options, option => option.selected).map(option => option.text);

//     var dockerfile = "FROM ubuntu:18.04\nRUN apt-get update && apt-get install -y \\\n\t"

//     for(var tool in selectedtools){
//         dockerfile += selectedtools[tool] + " \\ \n\t"
//     }

//     dockerfile += "&& rm -rf /var/lib/apt/lists/*"

//     console.log(dockerfile)

//     this.submit();



// })