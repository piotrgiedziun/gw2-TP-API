(function($){    
          var
            Item = Backbone.Model.extend(),
            
            Trends = Backbone.Collection.extend({
                Model: Item,
                url: "/api/get_trends"
            }),

            trends = new Trends(),
            MainView, TrendView, AddView;

          MainView = Backbone.View.extend({
           
            el: '#container',

            initialize: function() {
              this.template = _.template($('#template_main').html());
              this.render();
            },

            render: function() {

              var el = this.$el

              el.empty();
              el.append(this.template());

              trends.fetch();

              var trendView = new TrendView({collection: trends});
              el.append(trendView.render().el);

              return this;
            }
   
          });

          TrendView = Backbone.View.extend({
              
              el: '#trend_list',

              initialize: function() {
                  this.collection.bind('all', this.render,this);
                  this.template = _.template($('#template_item').html());
              },

              render:function (eventName) {
                var template = this.template,
                          el = this.$el,
                  collection = this.collection;
                
                if(collection.length == 0) return this;

                el.empty();

                collection.each(function(item){
                    el.append(template(item.toJSON()));
                });
                
                return this;
              }
          });

          AppRouter = Backbone.Router.extend({

            routes:{
                "":"home",
                "get:id":"get"
            },

            home:function() {
              new MainView();
            },

            get:function() {
              //soon
            }

          });

        }(jQuery));