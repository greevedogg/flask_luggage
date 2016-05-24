;(function() {
    'use strict';

    Vue.config.delimiters = ['${', '}'];
    Vue.config.unsafeDelimiters = ['{!!', '!!}'];

    new Vue({
        el: 'body',
        data: {
            binsToPersist: {},
            selectedBins: []
        },
        methods: {
            persistLocations: function(binsToPersist) {
                this.binsToPersist = binsToPersist;
            },
            openDialog: function() {
                $('.bin-location-finder').fadeIn(200);
            }
        },
        computed: {
            hasBins: function() {
                var bins = [];

                _.forOwn(this.binsToPersist, function(value, key) {
                    if (value) {
                        bins.push(key);
                    }
                });

                this.$set('selectedBins', bins);

                return bins.length > 0;
            }
        },
        events: {
            'current-locations': function(locations) {
                this.binsToPersist = locations;
            }
        }
    });
})();

