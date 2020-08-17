  function payWithPaystack(){
 	var amount = document.getElementById('amount').value;
    var handler = PaystackPop.setup({
      key: 'pk_test_90e512b1735b6d9527bbce412e5b22dae298afee',
      email: customer_email,
      amount: amount * 100,
      ref: ''+Math.floor((Math.random() * 10000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
      metadata: {
         custom_fields: [
            {
                display_name: phone_number,
                variable_name: phone_number,
                value: phone_number
            }
         ]
      },
      callback: function(response){
          alert('success. transaction ref is ' + response.reference);
          $.ajax({
            type: 'POST',
            url: fund_account,
            dataType: 'json',
            success: function(feedback){
                alert(feedback['message']);
                console.log(feedback["message"]);
                window.location = ORDER_SUMMARY_URL+"?ref="+response.reference;
             },
            error: function(xhr, status, error){
                 console.log('xhr: ' + xhr);
                 console.log('status: ' + status);
                  console.log("Error log: " + error['error']);
                    },
                });
      },
      onClose: function(){
          alert('window closed');
      }
    });
    handler.openIframe();
  }
function payWithPaystacsk(){
    //order variable
    //alert('serialized data: ' + $('.checkout-form').serialize());
    $('#payWithPaystackBtn').attr('value', 'Please Wait');
    user_id = $('.checkout-form #userIdInput').val();
    biller_phone = $('.checkout-form #phoneNumberInput').val();
    biller_address = $('.checkout-form #current_addressInput').val();
    biller_city = $('.checkout-form #cityInput').val();
    biller_state = $('.checkout-form #stateInput').val();
    biller_country = $('.checkout-form #countryInput').val();
    order_data = $('.checkout-form').serialize()
    //validation variables
    $current_address = notempty("current_addressInput");
    $city = notempty("cityInput");
    if($current_address == false){
        alert("address field is empty");
    }else if($city == false){
        alert("city is not entered.");
    }else{
        console.log("Information: " + order_data);
        var handler = PaystackPop.setup({
            key: $public_key,
            email: $customer_email,
            amount: $amount * 100,
            //ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
            metadata: {
                custom_fields: [
                    {
                        display_name: $phone_number,
                        variable_name: $phone_number,
                        value: $phone_number
                    }
                ]
            },
            callback: function(response){
                $('#payWithPaystackBtn').attr('value', 'PAY WITH PAYSTACK');
                alert('success. transaction ref is ' + response.reference);
                console.log('ORDER URL: ' + ORDER_URL +' ORDER SUMMARY: ' + ORDER_SUMMARY_URL );
                $.ajax({
                    type: 'POST',
                    url: ORDER_URL,
                    data: order_data+"&payment_mode=paystack&order_reference="+response.reference,
                    dataType: 'json',
                    success: function(feedback){
                        alert(feedback['message']);
                        console.log(feedback["message"]);
                        window.location = ORDER_SUMMARY_URL+"?ref="+response.reference;
                    },
                    error: function(xhr, status, error){
                        console.log('xhr: ' + xhr);
                        console.log('status: ' + status);
                        console.log("Error log: " + error['error']);
                    }
                });
            },
            onClose: function(){
                //alert('window closed');
            }
        });
        handler.openIframe();
    }
}

function notempty(id){
    // we grab the id value passed in the function
    var value = $("#"+id).val();
    // we get the character length
    var len = value.length;
    // check if the lenght is less then 1 character, you can change this value to check if less than 3 characters
    if (len < 1){
        return false;
    }else{
        return true;
    }
}
//pay on delivery
function payOnDelivery(){
    check = confirm("You are paying on delivery ?");
    if(check){
        $('#onDeliverProgress').fadeIn(200);
        user_id = $('.checkout-form #userIdInput').val();
        biller_phone = $('.checkout-form #phoneNumberInput').val();
        biller_address = $('.checkout-form #current_addressInput').val();
        biller_city = $('.checkout-form #cityInput').val();
        biller_state = $('.checkout-form #stateInput').val();
        biller_country = $('.checkout-form #countryInput').val();
        order_data = $('.checkout-form').serialize()
        //validation variables
        $current_address = notempty("current_addressInput");
        $city = notempty("cityInput");
        if($current_address == false){
            alert("address field is empty");
        }else if($city == false){
            alert("city is not entered.")
        }else {
            $order_reference = Date.now();
            console.log("Information: " + order_data);
            console.log("Order reference " + $order_reference);
            console.log('ORDER URL: ' + ORDER_URL + ' ORDER SUMMARY: ' + ORDER_SUMMARY_URL);
            $.ajax({
                type: 'POST',
                url: ORDER_URL,
                data: order_data + "&payment_mode=payondelivery&order_reference=" + $order_reference,
                dataType: 'json',
                success: function (feedback) {
                    alert(feedback['message']);
                    console.log(feedback["message"]);
                    window.location = ORDER_SUMMARY_URL + "?ref=" + $order_reference;
                    $('#onDeliverProgress').fadeOut(200);
                },
                error: function (xhr, status, error) {
                    console.log('xhr: ' + xhr);
                    console.log('status: ' + status);
                    console.log("Error log: " + error);
                    $('#onDeliverProgress').fadeOut(200);
                }
            });
        }
    }
}