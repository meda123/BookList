$(document).ready(function(){
    // $("#sortable").sortable();



    // Hides "rest books in each list upon page load"
    $(".hidden-list-segment").hide();

    // Hides "rest books until show is selected"
    $(".hide2").click(function(){

        var listId = $(this).data("list-id");
        $("#rest-of-books-" + listId).hide();
        $("#show-button-" + listId).show();
        $("#hide-button-" + listId).hide();
    });


    // Shows rest of books // 
    $(".show2").click(function(){

        var listId = $(this).data("list-id");
        $("#rest-of-books-" + listId).show();
        $("#show-button-" + listId).hide();
        $("#hide-button-" + listId).show();

    });
           

    // Manages Boolean values for read/unread check boxes 
    $('.bookRead').on('click', function() {
        bookId = $(this).data('book_id');
        checked = $(this).is(':checked');

        console.log("Element " + bookId + " is now " + checked);
        //saveBook(bookId, checked);

        $.post('/book_read', {id:bookId, read:checked});

    });
});
