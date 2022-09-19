 $(document).ready(function(){
            //Contact form Handler
            var contactForm = $(".contact-form")
            var contactFormEndpoint = contactForm.attr("action")
            var contactFormMethod = contactForm.attr("method")
            contactForm.submit(function(event){
                event.preventDefault()
                var formData = contactForm.serialize()
                $.ajax({
                    method: contactFormMethod,
                    url: contactFormEndpoint,
                    data: formData,
                    success: function(){
                       contactForm[0].reset()
                       $.alert({
                            title: 'Sent!',
                            content: 'Thank you for your submission!',
                            theme: 'modern',
                        });
                    },
                    error: function(){
                       $.alert({
                            title: 'Oops!',
                            content: 'An Error Occurred!\nPlease Try again!',
                            theme: 'modern',
                        });
                    }
                })
            })

            //For AutoSearch
            var searchForm = $('.search-form');
            searchForm = $(this)
            var searchInput = searchForm.find("[name = 'q']");
            var typingTimer;
            var typingInterval = 1000; //in millisecond
            var submitBtn = searchForm.find("[type = 'submit']")
            function performSearch(){
                doSearch();
                var query = searchInput.val();
                setTimeout(function(event){
                    window.location.href = "/search/?q=" + query;
                }, 3000)
            }
            function doSearch(){
                submitBtn.addClass("disabled")
                submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Searching....")
            }
            searchInput.keyup(function(event){
                // Key released
                clearTimeout(typingTimer)
                typingTimer = setTimeout(performSearch, typingInterval)
            })
            searchInput.keydown(function(event){
                // Key pressed
                clearTimeout(typingTimer)
            })
            //For Cart/ Products add/remove
            var productForm = $(".form-product-ajax") // #form-product-ajax
            productForm.submit(function(event){
                event.preventDefault();
                var thisForm = $(this);
                var actionEndpoint = thisForm.attr("data-endpoint");
                var httpMethod = thisForm.attr("method");
                var formData = thisForm.serialize();
                $.ajax({
                  url: actionEndpoint,
                  method: httpMethod,
                  data: formData,
                  success: function(data){
                    var submitSpan = $(".submit-span")
                    if(data.added){
                        submitSpan.html("<input type='submit' class='btn btn-warning' value='Remove from cart'>")
                    } else{
                        submitSpan.html("<input type='submit' class='btn btn-success' value='Add to cart'>")
                    }
                    var navCount = $("#navbar-cart-count")
                    navCount.text(data.count)
                    var currentPath = window.location.href
                    if(currentPath.indexOf("cart") != -1)
                    {
                        refreshCart()
                    }
                  },
                  error: function(errorData){
                    $.alert({
                        title: 'Oops!',
                        content: 'An Error Occurred!\nPlease Try again Later',
                    });
                  }
                })
            })

            function refreshCart()
            {
                var cartBody = $(".wrapper");
                var productRows = cartBody.find(".product-rows")
                var refreshCartUrl = "/api/cart/";
                var refreshCartMethod = 'GET';
                var data = {};
                var currentUrl = window.location.href
                $.ajax({
                    url: refreshCartUrl,
                    method: refreshCartMethod,
                    data: data,
                    success: function(data){
                        if (data.posts.length > 0)
                        {
                            var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                            productRows.html("")
                            $.each(data.posts, function(index, value){
                                var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                                newCartItemRemove.css('display', 'block')
                                newCartItemRemove.find('#cart-item-id').val(" " + value.id)
                                console.log(value)
                                productRows.append("<div class='row'><div class='col-2'>" + (index+1) +"</div><div class='col-8'><a href='" + value.url + "'>"+ value.message+"</a></div><div class='col-2'>"+ value.price +"</div></div><div class='row'><div class='col-12'>" + newCartItemRemove.html() + "</div><br><div class='col-12'><hr></div></div>")
                            })
                            cartBody.find("#cart-subtotal").text(data.subtotal)
                            cartBody.find("#cart-total").text(data.total)
                        }else{
                            window.location.href = currentUrl
                        }
                    },
                    error: function(errorData){
                       $.alert({
                        title: 'Oops!',
                        content: 'An Error Occurred!\nPlease Try again Later',
                       });
                    },
                })
            }
     })