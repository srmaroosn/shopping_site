var updatebtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updatebtns.length; i++) {
    updatebtns[i].addEventListener('click', function () {
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('product ID:', productID, 'action:', action)

        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            adddCookieItem(productID, action)

        }
        else {
            updateUserOrder(productID, action)

        }
    })
}

function adddCookieItem(productID, action) {
    console.log("Not logged in...")
    if (action == 'add') {
        if (cart[productID] == undefined) {
            cart[productID] = { 'quantity': 1 }
        }
        else {
            cart[productID]['quantity'] += 1
        }
    }
    if (action == 'remove') {
        cart[productID]['quantity'] -= 1
        
        if (cart[productID]['quantity'] <= 0) {
            console.log('item should be deleted')
            delete cart[productID]

        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart='+ JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}





function updateUserOrder(productID, action) {
    console.log("You are about to logged in.")
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productID': productID, 'action': action })
    })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()


        });


}