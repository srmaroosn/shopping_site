var updatebtns = document.getElementsByClassName('update-cart')
for(var i=0; i<updatebtns.length;i++){
    updatebtns[i].addEventListener('click', function(){
        var productID= this.dataset.product
        var action = this.dataset.action
        console.log('product ID:',productID, 'action:',action)

        console.log('USER:', user)
        if(user=='AnonymousUser'){
            console.log("User is not logged  in.")

        }
        else{
            updateUserOrder(productID, action)
           
        }
    })
}
function updateUserOrder(productID, action){
    console.log("You are about to logged in.")
    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productID': productID, 'action':action})
    })

    .then((response) =>{
        return response.json();
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()

   
    });


}