if (window.location.pathname == "/") {
    let today = new Date();
    let date = today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate();
    document.getElementsByClassName("date")[0].innerHTML = date
}

let value = $(".value");
let plus = $(".plus");
let mins = $(".mins");
let deletCart = $(".deletCart");

for (let p = 0; p < plus.length; p++) {
    const element = plus[p];
    $(element).on("click", function () {
        $(value[p]).attr("value", parseFloat($(value[p]).attr("value").replace(",", ".")) + parseFloat($(value[p]).attr("data-upTo").replace(",", ".")));
        data = {
            productId: $(value[p]).attr("data-productId"),
            quantity: $(value[p]).attr("value"),
            add: "add",
        }
        send_data(data, window.location.href, (res) => {
            console.log(res);
            $(".total").text(res.total)
            $(".countCart").text(res.cartCount)

            if (res.inCart) {
                let comp = `<p id="itemsId${res.data.product.id}">${res.data.product.title}<span class="btn btn-sm btn-danger deletCart" data-productId="${res.data.product.id}">ازالة</span></p>`
                $(".itemsCart").prepend(comp)
            }

        });
    });
}


for (let m = 0; m < mins.length; m++) {
    const element = mins[m];
    $(element).on("click", function () {
        $(value[m]).attr("value", parseFloat($(value[m]).attr("value").replace(",", ".")) - parseFloat($(value[m]).attr("data-upTo").replace(",", ".")));
        data = {
            productId: $(value[m]).attr("data-productId"),
            quantity: $(value[m]).attr("value"),
            mins: "mins"
        }
        if (parseFloat($(value[m]).attr("value")) <= 0.0) {
            $(value[m]).attr("value", 0);
        }
        send_data(data, window.location.href, (res) => {
            $(".countCart").text(res.cartCount)
            $(".total").text(res.total)
            if (res.data.quantity == 0) {
                $(`#itemsId${res.data.product.id}`).remove();
            }
        });
    });
}

//استخدمت الطريقة دي عشان لما احط عنصر جديد الزرار يشتغل
$('body').on('click', '.deletCart', function () {

    data = {
        productId: $(this).attr("data-productId"),
        deletCart: "deletCart"
    }
    send_data(data, window.location.href, (res) => {
        $(".countCart").text(res.cartCount)
        $(".total").text(res.total)
        $(`#itemsId${res.data.product.id}`).remove();
        $(`[data-productId="${res.data.product.id}"]`).attr('value', 0);
    });
});





$(".Redeem").on("click", function (e) {
    console.log("here");
    e.preventDefault();
    var data = {
        PromoCode: "PromoCode",
        poromoText: $(".poromoText")[0].value,
    };
    send_data(data, window.location.href, (res) => {
        $("#codeing").attr("value", data.poromoText);
        let new_price = res.price.toFixed(2);
        $(".total_price").text(new_price);
        if (res.message == false) {
            $(".poromoText").addClass("is-invalid");
        } else {
            $(".poromoText").addClass("is-valid");
            $(".poromoText").attr("disabled", "");
            $(".poromoText").removeClass("is-invalid");
        }
    });
});



//دي الطريقة القديمة بتنقع للحاجت اللي مش بتعوز شغل live
// for (let d = 0; d < deletCart.length; d++) {
//     const element = deletCart[d];
//     $(element).on("click", function () {

//         data = {
//             productId: $(this).attr("data-productId"),
//             deletCart: "deletCart"
//         }
//         send_data(data, window.location.href, (res) => {
//             $(".total").text(res.total)
//             $(`#itemsId${res.data.product.id}`).remove();
//             document.querySelector(`[data-productId="${res.data.product.id}"]`).value = 0
//         });
//     });
// }