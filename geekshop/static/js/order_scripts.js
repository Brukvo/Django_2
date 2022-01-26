window.onload = function () {
    let qty, price, orderitem_num, delta_qty, orderitem_qty, delta_cost

    let qty_arr = []
    let price_arr = []

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())

    let order_total_qty = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;

    for(let i = 0; i < total_forms; i++){
        qty = parseInt($('input[name=orderitems-' + i + '-quantity]').val())
        price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'))

        qty_arr[i] = qty;

        if(price){
            price_arr[i] = price;
        }
        else {
            price_arr[i] = 0;
        }
    }

    // 1
    $('.order_form').on('click', 'input[type=number]', function(){
        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        if(price_arr[orderitem_num]){
            orderitem_qty = parseInt(target.value);
            delta_qty = orderitem_qty - qty_arr[orderitem_num];
            qty_arr[orderitem_num] = orderitem_qty;
            orderSummaryUpdate(price_arr[orderitem_num], delta_qty)
        }
    })

    // 2
    $('.order_form').on('click', 'input[type=checkbox]', function(){
        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''))
        if(target.checked){
            delta_qty = -qty_arr[orderitem_num]
        }
        else {
            delta_qty = qty_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_qty)
    });


    function orderSummaryUpdate(orderitem_price, delta_qty) {
        delta_cost = orderitem_price * delta_qty;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_qty = order_total_qty + delta_qty;

        $('.order_total_quantity').html(order_total_qty.toString());
        $('.order_total_cost').html(order_total_cost.toString() + ',00');


    }

    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить товар',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    function deleteOrderItem(row){
        let target_name = row[0].querySelector('input[type="number"]').name
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''))
        delta_qty = -qty_arr[orderitem_num]
        orderSummaryUpdate(price_arr[orderitem_num], delta_qty)
    }

}