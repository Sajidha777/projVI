$(document).ready(function(){
    //LOAD MORE 
    $("#loadMore").on('click',function(){
        var _currentProducts=$(".product-box").length; 
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');
        console.log(_currentProducts,_limit,_total);

        //AJAX
        $.ajax({
            url:'/load-more-data',
            data:{
                limit:_limit,
                offset:_currentProducts,
            },
            datatype:'json',
            beforeSend:function(){
                $("#loadMore").attr('disabled',true);
                $(".load-more-icon").addClass('fa-spin');
            },
            success:function(res){
                $("#filteredProducts").append(res.data);
                $("#loadMore").attr('disabled',false);
                $(".load-more-icon").removeClass('fa-spin');
            
                var _totalShowing=$(".product-box").length;
                if(_totalShowing==_total){
                    $("#loadMore").remove();
                }
            }
        });
        //END AJAX
    });
    //END LOADMORE


    //PRODUCT VARIATION
    $(".choose-size").hide();

	//Show size and image according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-color").removeClass('focused');
		$(this).addClass('focused');

		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color"+_color).first().addClass('active');

        //image according to selected color
        var _image=$(".color"+_color).first().attr('data-image');
        $("#zoom_01").attr('data-zoom-image',_image);
        $("#zoom_01").attr('src',_image);


        //price according to selected color
		var _price=$(".color"+_color).first().attr('data-price');
		$(".product-price").text(_price);

        //for cart
        _imageforcart=$(".color"+_color).first().attr('data-image-cart');
        _idforcart=$(".color"+_color).first().attr('data-id');
        

	});
	// End

	// Show the price according to selected size
	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');     

        //image according to selected size
        var _image=$(this).attr('data-image');
        $("#zoom_01").attr('data-zoom-image',_image);
        $("#zoom_01").attr('src',_image);

        //price according to selected size
		var _price=$(this).attr('data-price');
		$(".product-price").text(_price);

        //for cart
        _imageforcart=$(this).attr('data-image-cart');
        _idforcart=$(this).attr('data-id');
	})
	// End


	// Show the first selected color
	$(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
    var _price=$(".color"+_color).first().attr('data-price');
	
	$(".color"+_color).show();
	$(".color"+_color).first().addClass('active');
	$(".product-price").text(_price);

    //for cart
    _imageforcart=$(".color"+_color).first().attr('data-image-cart');
    _idforcart=$(".color"+_color).first().attr('data-id');
    //END PRODUCTVARIATION


    //ADD TO CART from list pages
    $(document).on('click',".add-to-cart ",function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productAttrId=$(".product-id-"+_index).attr('data-id');
        var _productTitle=$(".product-title-"+_index).val();
        var _productImage=$(".product-image-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();
        console.log(_qty,_productAttrId,_productTitle,_productImage,_productPrice);

        //Ajax Request
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_productAttrId,
                'prodid':_index,
                'qty':_qty,
                'image':_productImage,
                'title':_productTitle,
                'price':_productPrice,
            },
            datatype:'json',
            beforeSend:function(){
                //disable clicking the button again while already sending data
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                //enable the button when sending data is complete
                _vm.attr('disabled',false);
            }
        });
        //END AJAX


    });
    //END ADD TO CART

    //ADD TO CART on productdetail page
    $(document).on('click',".add-to-cart-detail-page ",function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productAttrId=_idforcart;
        var _productTitle=$(".product-title-"+_index).val();
        var _productImage=_imageforcart;
        var _productPrice=$(".product-price-"+_index).text();

        console.log(_qty,_productAttrId,_productTitle,_productImage,_productPrice);
        //Ajax Request
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_productAttrId,
                'prodid':_index,
                'qty':_qty,
                'image':_productImage,
                'title':_productTitle,
                'price':_productPrice,
            },
            datatype:'json',
            beforeSend:function(){
                //disable clicking the button again while already sending data
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                //enable the button when sending data is complete
                _vm.attr('disabled',false);
            }
        });
        //END AJAX
    });
    //END ADD TO CART from product detail page

    //DELETE ITEM FROM CART
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		
	});
    //END DELETE

    //UPDATE ITEM FROM CART
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
	
	});
    	// END UPDATE CART

});