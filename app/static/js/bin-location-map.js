;(function(){
    'use strict';

    var observe = $({});
    var binToPersist = null;

    observe.on('location:selected', function(e, mapIdentifier) {
        binToPersist = mapIdentifier;
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

            observe.trigger('location:selected', [mapIdentifier]);
    //        event.preventDefault();
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