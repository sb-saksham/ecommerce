var key = $('key').val()
var hash_string = $('hash_string').val()
var hash = $('hash').val()
var txnid = $('txnid').val()
var amount = $('amount').val()
var firstname = $('firstname').val()
var phone = $('phone').val()
var productinfo = $('productinfo').val()
var surl = $('surl').val()
var furl = $('furl').val()
var service_provider = 'payu_paisa'

var RequestData = {
      'key': key,
      'txnid':txnid,
      'hash':hash,
      'amount':amount,
      'firstname':firstname,
      'email':email,
      'phone':phone,
      'productinfo':productinfo,
      'surl':surl,
      'furl':furl,
      'service_provider':service_provider,
  }


var Handler = {

      responseHandler: function(BOLT){

        // your payment response Code goes here, BOLT is the response object
        $.alert('<strong>The payment is SUCCESSFULL</strong>')

      },
      catchException: function(BOLT){

        // the code you use to handle the integration errors goes here
        $.alert('The payment FAILED')

      }
  }

    $('#pay_now').onclick(function(){
        bolt.launch(RequestData,Handler)
    })
