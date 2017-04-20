$(document).ready(function(){
    // $("#sortable").sortable();



    // Hides "rest books in each list upon page load"
    $("#rest-of-books").hide();

    // Hides "rest books until show is selected"
    $("#hide").click(function(){
        $("#rest-of-books").hide();
    });

    // Shows top5 books // 
    $("#show").click(function(){
        $("#rest-of-books").show();
    });
       



    // Manages Boolean values for read/unread check boxes 
    $('.bookRead').on('click', function() {
        listId = $(this).data('book_id');
        checked = $(this).is(':checked');

        console.log("Element " + listId + " is now " + checked);
        //saveBook(listId, checked);

    $.post("/book_read", {id:listId, read:checked});

    });
});


