;(function(){
    'use strict';

    var observe = $({});
    var binToPersist = null;

    observe.on('location:selected', function(e, selectedBin, mapIdentifier) {
        var $selectedBin = $(selectedBin);

        binToPersist = mapIdentifier;

        observe.trigger('location:clear-selected');

        if ($selectedBin.is('.overlay__location')) {
            $selectedBin.addClass('overlay__location--selected');
        }
    });

    observe.on('location:clear-selected', function() {
        $('.overlay__location').removeClass('overlay__location--selected');
    });

    observe.on('location:persist', function() {
        $('#location').val(binToPersist);

        observe.trigger('location:reset');
    });

    observe.on('location:reset', function() {
        binToPersist = null;
    });

    $(function(){
        // bin location overlay component
        if ($('html').is('.is-desktop')) {
            $('.overlay__content').addClass('overlay__content--desktop');
        }

        $('#view-bin-availability').click(function(event) {
           $('#bin-location-finder').fadeIn(200);

            event.preventDefault();
        });

        $('.overlay__location').on('click touchstart', function(event) {
            var mapIdentifier = $(this).data('map-identifier');

            observe.trigger('location:selected', [event.currentTarget, mapIdentifier]);

            event.preventDefault();
        });

        $('.overlay__save').click(function(event) {
            $('#bin-location-finder').fadeOut(200);

            observe.trigger('location:persist');

            event.preventDefault();
        });

        $('.overlay__cancel').click(function(event) {
            $('#bin-location-finder').fadeOut(200);

            observe.trigger('location:reset');

            event.preventDefault();
        });
    });
})();