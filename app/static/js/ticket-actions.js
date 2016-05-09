;(function(){
    'use strict';

    $(function(){
        var completeTicketURL;
        var partyName;
        var $myModal = $('#myModal');
        
        $myModal.on('show.bs.modal', function(e) {
            $("#dialog__close-ticket__party-name").text(partyName);
        });

        $('.ticket-actions__complete').on('click touchstart', function(event) {
            completeTicketURL = $(this).attr('href');
            partyName = $(this).data('partyName');
            $myModal.modal('show');

            event.preventDefault();
        });

        $('.dialog__close-ticket__close').on('click touchstart', function(event) {
            $myModal.modal('hide');
            event.preventDefault();
            var initials = $('#dialog__close-ticket-initials').val();

            window.location = completeTicketURL+'?loggedOutBy='+initials;
        });
    });
})();