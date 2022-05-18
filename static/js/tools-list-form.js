var form = document.getElementById('myForm')

form.addEventListener('submit',function(event){
    event.preventDefault()

    var lst = document.querySelector('#list')
    var selectedlist = [].filter.call(lst.options, option => option.selected).map(option => option.text);
    console.log(selectedlist[0])



})