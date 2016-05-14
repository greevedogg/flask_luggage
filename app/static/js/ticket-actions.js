;(function(){
    'use strict';

    $(function(){
        var completeTicketURL;

        var closeTicketDialog = new CloseTicketDialog({
            buttonAccept: 'Close Ticket',
            acceptCallback: function() {
                closeTicketDialog.hide();
                var initials = $('#dialog__close-ticket-initials').val();

                window.location = completeTicketURL+'?loggedOutBy='+initials;
            }
        });

        $('.ticket-actions__complete').on('click touchstart', function(event) {
            completeTicketURL = $(this).attr('href');
            var partyName = $(this).data('partyName');

            closeTicketDialog.setParty(partyName);
            closeTicketDialog.show();

            event.preventDefault();
        });
    });
})();
