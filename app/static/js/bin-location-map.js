;(function(){
    'use strict';

    $(function() {
        // bin location overlay component
        if ($('html').is('.is-desktop')) {
            $('.overlay__content').addClass('overlay__content--desktop');
        }
    });

    Vue.component('bin-location-map', {
        template: '#bin-location-map-template',
        props: {
            binsToPersist: {
                type: Object,
                default: function() {
                    return {};
                }
            }
        },
        data: function() {
            return {
                selectedMapIdentifier: null,
                touchedEnded: false
            };
        },
        activate: function (done) {
            if (this.binsToPersist) {
                this.broadcastCurrentLocations(this.binsToPersist); // TODO: I'm not liking this. I think there could be a better way of communicating to child components that binsToPersist has been set.
            }

            done();
        },
        methods: {
            save: function() {
                $('.bin-location-finder').fadeOut(200);

                this.persistLocations();
            },
            cancel: function() {
                $('.bin-location-finder').fadeOut(200);

                this.resetLocations();
            },
            persistLocations: function() {
                this.$dispatch('persist-locations', this.binsToPersist);
            },
            resetLocations: function() {
                var that = this;

                _.forOwn(this.binsToPersist, function(value, key) {
                    Vue.set(that.binsToPersist, key, 0);
                });

                this.$dispatch('current-locations', this.binsToPersist);
                this.broadcastCurrentLocations(this.binsToPersist);
            },
            broadcastCurrentLocations: function (binsToPersist) {
                this.$broadcast('current-locations', binsToPersist);
            },
            selectedLocation: function(event, mapIdentifier, isTouch) {
                var isTouch = isTouch || false;

                this.selectedMapIdentifier = mapIdentifier;

                if (event.metaKey || (isTouch && this.touchedEnded == false)) {
                    this.addLocation(mapIdentifier);
                } else {
                    this.oneLocation(mapIdentifier);
                    this.touchedEnded = false;
                }

                this.$dispatch('current-locations', this.binsToPersist);
                this.broadcastCurrentLocations(this.binsToPersist);
            },
            addLocation: function(location) {
                Vue.set(this.binsToPersist, location, 1);
            },
            removeLocation: function(location) {
                Vue.delete(this.binsToPersist, location);
            },
            oneLocation: function(location) {
                this.resetLocations();
                this.addLocation(location);
            },

        },
        events: {
            'selected-location': function(event, mapIdentifier, isTouch) {
                this.selectedLocation(event, mapIdentifier, isTouch);
            },
            'touch-ended': function() {
                this.touchedEnded = true;
            }
        }
    });

    Vue.component('map-location', {
        template: '#location-template',
        // props: ['location', 'map-identifier', 'is-occupied', 'amount'],
        props: {
            location: null,
            mapIdentifier: null,
            isOccupied: {
                default: false
            },
            amount: null
        },
        data: function() {
            return {
                currentLocations: {}
            }
        },
        computed: {
            isSelected: function() {
                return this.mapIdentifier in this.currentLocations && this.currentLocations[this.mapIdentifier];
            }
        },
        methods: {
            selectedLocation: function(event) {
                this.isSelected = true;

                var mapIdentifier = $(event.currentTarget).data('map-identifier');

                this.$dispatch('selected-location', event, mapIdentifier);
            },
            touchStartedLocation: function(event) {
                var mapIdentifier = null;


                if (event.targetTouches && event.targetTouches.length > 0) {
                    mapIdentifier = $(event.currentTarget).data('map-identifier');
                }
                
                this.$dispatch('touch-started');
                this.$dispatch('selected-location', event, mapIdentifier, true);
            },
            touchEndedLocation: function(event) {
                this.$dispatch('touch-ended');
            }
        },
        events: {
            'current-locations': function(locations) {
                this.currentLocations = locations;
            }
        }
    });
})();