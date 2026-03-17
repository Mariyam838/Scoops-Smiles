from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import sqlite3, os, json

app = Flask(__name__)
app.secret_key = "icecream_shop_2024"
DB = "orders.db"

# ─────────────────────────────────────────
# PRODUCT DATA
# ─────────────────────────────────────────

CONES = [
    {"id":101,"name":"Classic Vanilla Cone",       "price":12.00,"desc":"Silky smooth vanilla bean ice cream in a crispy waffle cone. Made with real Madagascar vanilla.",          "img":"https://static.vecteezy.com/system/resources/previews/032/405/432/non_2x/vanilla-ice-cream-in-cone-with-flying-ingredients-in-the-air-on-pastel-background-ai-generated-photo.jpg"},
    {"id":102,"name":"Double Chocolate Cone",       "price":14.00,"desc":"Rich dark chocolate ice cream double-scooped in a chocolate-dipped waffle cone.",                        "img":"https://lumenor.ai/cdn-cgi/imagedelivery/F5KOmplEz0rStV2qDKhYag/2324981f-fe2b-4c36-433b-eb150caf7900/tn"},
    {"id":103,"name":"Strawberry Cone",             "price":13.00,"desc":"Fresh strawberry ice cream bursting with real fruit pieces in a golden sugar cone.",                     "img":"https://static.vecteezy.com/system/resources/previews/058/099/640/large_2x/delicious-strawberry-ice-cream-cone-with-pink-drizzle-close-up-photo.jpg"},
    {"id":104,"name":"Mixed Swirl Cone",            "price":15.00,"desc":"Vanilla and chocolate swirled together in perfect harmony on a crispy waffle cone.",                     "img":"https://img.pikbest.com/origin/09/34/18/67EpIkbEsTzvy.jpg!sw800"},
    {"id":105,"name":"Blackberry Cone",             "price":11.00,"desc":"Classic creamy soft serve, perfectly swirled to a signature peak in a fresh waffle cone.",              "img":"https://png.pngtree.com/thumb_back/fh260/background/20241210/pngtree-a-creative-ice-cream-cone-with-juicy-blackberries-and-splash-of-image_16749595.jpg"},
    {"id":106,"name":"Mint Choc Chip Cone",         "price":14.00,"desc":"Cool peppermint ice cream loaded with dark chocolate chips in a sugar cone.",                           "img":"https://static.vecteezy.com/system/resources/thumbnails/059/946/349/small_2x/enjoy-mint-chocolate-chip-ice-cream-cone-in-a-playful-summer-setting-alongside-mint-leaves-and-chocolate-chips-photo.jpeg"},
    {"id":107,"name":"Pistachio Cone",              "price":16.00,"desc":"Premium pistachio ice cream with real crushed pistachios in a golden waffle cone.",                     "img":"https://thumbs.dreamstime.com/b/pistachio-ice-cream-drizzled-chocolate-sauce-waffle-cones-two-scoops-laying-slate-surface-accompanied-395488553.jpg"},
    {"id":108,"name":"Caramel Crunch Cone",         "price":15.00,"desc":"Salted caramel ice cream with caramel ribbon and toffee crunch pieces.",                               "img":"https://img.freepik.com/premium-photo/soft-serve-ice-cream-cone-with-caramel-sauce_777078-29403.jpg"},
    {"id":109,"name":"Cookies & Cream Cone",        "price":14.00,"desc":"Vanilla ice cream packed with crushed Oreo cookies on a chocolate waffle cone.",                       "img":"https://images.squarespace-cdn.com/content/v1/525d98f0e4b0f07bb3deb091/1595432694724-NEKGEOJ07KJ3ZZ249A23/Classic+Cookies+and+Cream+Ice+Cream"},
    {"id":110,"name":"Bubblegum Rainbow Cone",      "price":13.00,"desc":"Fun bubblegum flavoured ice cream with rainbow sprinkles — a kids' favourite.",                        "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx0b4y2rrWpYQJY-87FavXa18yoWuurkUJTg&s"},
    {"id":111,"name":"Mango Sorbet Cone",           "price":13.00,"desc":"Refreshing alphonso mango sorbet, dairy-free and bursting with tropical flavour.",                     "img":"https://thumbs.dreamstime.com/b/refreshing-yellow-mango-ice-cream-scoop-waffle-cone-wooden-table-juicy-slices-372311739.jpg"},
    {"id":112,"name":"Rocky Road Cone",             "price":15.00,"desc":"Chocolate ice cream with marshmallows, almonds and chocolate chunks piled high.",                      "img":"https://t4.ftcdn.net/jpg/17/61/27/69/360_F_1761276930_4t5RbuI1GasaGHdM0vgRhtWMI95TZVB3.jpg"},
    {"id":113,"name":"Vanilla rasberry Cone",        "price":14.00,"desc":"Creamy vanilla base swirled with fresh blueberry compote in a pretzel cone.",                         "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxJJK7jrPNzeWAs_Ina3FAP9t3MTjgYBaPOw&s"},
    {"id":114,"name":"Tiramisu Cone",               "price":17.00,"desc":"Italian-inspired coffee and mascarpone ice cream dusted with cocoa powder.",                           "img":"https://cdn.donnahaycdn.com.au/images/content-images/tiramisu_swirl_ice-cream_waffle_cones.jpg"},
    {"id":115,"name":"Triple Berry Cone",           "price":14.00,"desc":"Strawberry, raspberry and blueberry trio ice cream in a classic sugar cone.",                          "img":"https://thumbs.dreamstime.com/b/tempting-triple-scoop-ice-cream-cone-berry-swirls-placed-against-tranquil-blue-sky-perfect-dessertthemed-artwork-326145870.jpg"},
    {"id":116,"name":"Peanut Butter Cone",          "price":15.00,"desc":"Rich peanut butter ice cream with chocolate chips and a honey drizzle.",                               "img":"https://img.freepik.com/premium-photo/ice-cream-cone-with-peanut-butter-drizzle_1169880-188853.jpg"},
]

CUPS = [
    {"id":201,"name":"Chocolate Fudge Cup",         "price":14.00,"desc":"Dense chocolate ice cream with hot fudge swirl and brownie chunks in a generous cup.",                 "img":"https://www.thebrooklyncreamery.com/cdn/shop/files/20-1.jpg?v=1748001085&width=2048"},
    {"id":202,"name":"Cookies & Cream Cup",         "price":14.00,"desc":"Vanilla ice cream overloaded with crushed Oreo cookies and cream swirl.",                             "img":"https://thumbs.dreamstime.com/b/creamy-delicious-vanilla-cookies-cream-ice-cream-cookies-cream-ice-cream-texture-background-creamy-delicious-395241935.jpg?w=992"},
    {"id":203,"name":"Mango Cream Cup",             "price":13.00,"desc":"Tropical mango ice cream with mango jelly pieces and a white chocolate drizzle.",                     "img":"https://thumbs.dreamstime.com/b/dessert-artisanal-mango-italian-ice-cream-gourmet-dessert-artisanal-mango-vanilla-italian-ice-cream-garnished-110202134.jpg?w=992"},
    {"id":204,"name":"Salted Caramel Cup",          "price":15.00,"desc":"Buttery salted caramel ice cream with caramel sauce and sea salt flakes on top.",                     "img":"https://www.thespruceeats.com/thmb/jZmYRDpWby4VM4r2w5Cah1Vth_U=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/SaltedCaramelIceCreamHERO-9e49945bc9fb4afca856e37f5b1bbbe5.jpg"},
    {"id":205,"name":"Strawberry Cheesecake Cup",   "price":16.00,"desc":"Strawberry ice cream on a graham cracker crumble base with cheesecake swirl.",                       "img":"https://t4.ftcdn.net/jpg/12/57/70/71/360_F_1257707104_hOUTAfFMbco5IENHwr3wl2ugddK1WmEL.jpg"},
    {"id":206,"name":"Mint Chip Cup",               "price":14.00,"desc":"Cool mint ice cream with dark chocolate chips and a chocolate syrup drizzle.",                        "img":"https://img.freepik.com/premium-photo/delicious-ice-cream-cup-with-mint-chocolate-chip-ice-cream_1354363-1424.jpg"},
    {"id":207,"name":"Birthday Cake Cup",           "price":15.00,"desc":"White cake-flavoured ice cream with rainbow sprinkles and frosting swirl.",                           "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSz-OOpDzoyxC0JjfZHjt6pPzAcm43LFawbfw&s"},
    {"id":208,"name":"Espresso Crunch Cup",         "price":16.00,"desc":"Bold espresso ice cream with toffee brittle and chocolate-covered espresso beans.",                   "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBZevXX6jO2ntJ_wMN1mNwFrddT3eAVwlKUw&s"},
    {"id":209,"name":"Lychee Rose Cup",             "price":15.00,"desc":"Delicate lychee ice cream with rose petal jam and dried rose buds. Exquisitely floral.",              "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuFh0VbUcry-94MKLeobugMIMoCFOm7pd3Fw&s"},
    {"id":210,"name":"Pineapple Coconut Cup",       "price":14.00,"desc":"Tropical pineapple and coconut ice cream with toasted coconut flakes.",                               "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGnQ6lgT3oi45eC4bnvuaU1fl1LXecGBKiiQ&s"},
    {"id":211,"name":"Hazelnut Praline Cup",        "price":17.00,"desc":"Ferrero-inspired hazelnut ice cream with praline chunks and chocolate sauce.",                        "img":"https://thumbs.dreamstime.com/b/delicious-hazelnut-praline-ice-cream-dessert-mint-garnish-371662535.jpg?w=992"},
    {"id":212,"name":"Blueberry Lavender Cup",      "price":15.00,"desc":"Unique lavender ice cream with fresh blueberry compote and honey drizzle.",                          "img":"https://images.squarespace-cdn.com/content/v1/525d98f0e4b0f07bb3deb091/1596545885272-54ENPBNTGLIQ7ZS386XH/Blueberry+Lavender+Crumble+Ice+Cream"},
    {"id":213,"name":"Black Sesame Cup",            "price":16.00,"desc":"Rich and nutty Japanese-inspired black sesame ice cream with mochi pieces.",                         "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3ui9ub-4C3KYsHbDasi4vYdEBotiEf8Zz5w&s"},
    {"id":214,"name":"Raspberry Ripple Cup",        "price":13.00,"desc":"Classic vanilla ice cream with vibrant raspberry ripple swirls throughout.",                          "img":"https://thumbs.dreamstime.com/b/raspberry-ripple-ice-cream-scoops-fresh-berries-square-raspberry-ripple-ice-cream-122670663.jpg?w=768"},
    {"id":215,"name":"Dulce de Leche Cup",          "price":15.00,"desc":"Argentine-style dulce de leche ice cream with caramel ribbons and biscuit bits.",                    "img":"https://www.jcookingodyssey.com/wp-content/uploads/2025/07/Dulce-De-Leche-ice-cream-500x500.jpg"},
]

CAKES = [
    {"id":301,"name":"Chocolate Fudge Ice Cream Cake","price":85.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Layers of dark chocolate ice cream and chocolate fudge between chocolate sponge layers, finished with ganache drip.","img":"https://img.freepik.com/premium-photo/chocolate-fudge-ice-cream-cake-platter_419341-99583.jpg"},
    {"id":302,"name":"Vanilla Birthday Cake",       "price":80.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Classic vanilla ice cream layered with vanilla sponge, covered in white whipped cream and rainbow sprinkles. Perfect for celebrations.","img":"https://www.sidechef.com/recipe/532fa185-a31e-477c-af58-4d6105b7e1bb.jpeg?d=1408x1120"},
    {"id":303,"name":"Oreo Ice Cream Cake",         "price":90.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Cookies & cream ice cream on an Oreo crust, topped with whipped cream and crushed Oreo crumble.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv7xeWomEeRg9h6dCnyWWZHhpwvrVOWcWypQ&s"},
    {"id":304,"name":"Strawberry Dream Cake",       "price":85.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Strawberry ice cream with fresh strawberry compote layers and strawberry swiss meringue buttercream frosting.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7U3d4es8b4XkkJV3y-GNgLSmWUF7izBcs_A&s"},
    {"id":305,"name":"Rainbow Unicorn Cake",        "price":95.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Multi-coloured ice cream layers — strawberry, mango, blueberry and vanilla — beneath white buttercream and unicorn decorations.","img":"https://recipesbyclare.com/assets/images/1737388005208-0cijod7v.webp"},
    {"id":306,"name":"Mint Chocolate Cake",         "price":88.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Peppermint ice cream between chocolate sponge, coated in dark chocolate ganache with mint leaves.","img":"https://www.rainbownourishments.com/wp-content/uploads/2022/01/vegan-mint-chocolate-chip-ice-cream-cake-1.jpg"},
    {"id":307,"name":"Caramel Praline Cake",        "price":92.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Salted caramel ice cream with praline crunch layers and caramel drip finish with gold leaf decoration.","img":"https://stellinasweets.com/wp-content/uploads/2017/01/new-orleans-ice-cream-cake-49.jpg"},
    {"id":308,"name":"Tiramisu Ice Cream Cake",     "price":98.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Coffee ice cream with espresso-soaked ladyfingers and mascarpone cream layers, dusted with cocoa.","img":"https://cdn.donnahaycdn.com.au/images/content-images/tiramisu_ice_cream_layer_cake.jpg"},
    {"id":309,"name":"Mango Cheesecake Ice Cream",  "price":90.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Mango ice cream on a cream cheese layer and biscuit base, topped with fresh mango glaze.","img":"https://bakewithzoha.com/wp-content/uploads/2025/06/no-bake-mango-cheesecake-4.jpg"},
    {"id":310,"name":"Hazelnut Rocher Cake",        "price":105.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Ferrero-inspired hazelnut ice cream cake with chocolate feuilletine crunch and golden hazelnut decoration.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR00uwTfuKZi3dhwhn2JL2Jg0eQcUSF0f29Yw&s"},
    {"id":311,"name":"Pistachio Rose Cake",         "price":95.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Pistachio ice cream with rosewater cream layers and crushed pistachio topping — Middle Eastern inspired.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRwWfSsVXupdehIle972ZkrA_o220pmBmGFw&s"},
    {"id":312,"name":"Red Velvet Ice Cream Cake",   "price":92.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Red velvet ice cream between moist red velvet sponge layers with cream cheese frosting.","img":"https://www.tasteandtellblog.com/wp-content/uploads/2024/08/Red-Velvet-Ice-Cream-Cake-3-768x1152.jpg"},
    {"id":313,"name":"Lemon Sorbet Cake",           "price":82.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Zesty lemon sorbet layered with vanilla sponge and lemon curd, finished with meringue kisses.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEPA-bPEk5MBAr09Me6KX1Pm0MfNoK1e-Jaw&s"},
    {"id":314,"name":"Biscoff Dream Cake",          "price":95.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Biscoff ice cream with speculoos crumble layers and a glossy caramel Biscoff drip on top.","img":"https://butteroverbae.com/wp-content/uploads/2020/08/Lotus-Biscoff-Ice-cream-cake-1.jpg"},
    {"id":315,"name":"Bubblegum Party Cake",        "price":88.00,"sizes":["6-inch · 6 pax","8-inch · 10 pax","10-inch · 16 pax"],"desc":"Bright pink bubblegum ice cream with colourful sprinkle layers — the ultimate kids' party cake.","img":"https://upload.wikimedia.org/wikipedia/commons/9/90/Rainbow_bubblegum_ice_cream_cake_ready_to_go_for_the_weekend_%2830125441560%29.jpg"},
]

FRUITSHAPED = [
    {"id":401,"name":"Mango Shaped Ice Cream",      "price":12.00,"desc":"Mango sorbet shaped and coloured exactly like a real mango. Deliciously fruity and stunning to look at.","img":"https://www.cookfastrecipes.com/wp-content/uploads/2025/06/viral-mango-ice-cream-tiktok.webp"},
    {"id":402,"name":"Watermelon Ice Bar",          "price":11.00,"desc":"Watermelon sorbet with chocolate chip seeds on a green coconut coating — iconic summer treat.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F4e6a0484-de86-4e60-b508-f011539216df.jpg"},
    {"id":403,"name":"Pineapple Ice Cream",         "price":12.00,"desc":"Tropical pineapple sorbet shaped like a whole pineapple with a white chocolate crown.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2Fe9233e16-d85e-44ce-8ce6-c9f369398d15.jpg"},
    {"id":404,"name":"Strawberry Shape Ice Cream",  "price":11.00,"desc":"Strawberry ice cream moulded into a perfect strawberry with dark chocolate seed dots.","img":"https://media.pixverse.ai/pixverse%2Fi2i%2Fori%2F1ce21fc0-be50-4208-b261-5936d7efe04b.jpg"},
    {"id":405,"name":"Coconut Shell Ice Cream",     "price":13.00,"desc":"Coconut ice cream served inside a real miniature coconut half shell with toasted flakes.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F6282a164-4a43-4ea9-9c48-ee7f1a1b5319.jpg"},
    {"id":406,"name":"Peach Ice Cream",             "price":12.00,"desc":"White peach sorbet shaped like a fuzzy peach with a red blush and green marzipan leaf.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2Faea7076e-2f77-47da-b9fe-70931ad9e2f3.jpg"},
    {"id":407,"name":"Grape Cluster Ice Cream",     "price":13.00,"desc":"Concord grape ice cream moulded into a realistic grape cluster — each grape a perfect bite.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2Ffa824d2e-81e6-4a22-b268-1b6afbd01616.jpg"},
    {"id":408,"name":"Lemon Ice Cream",             "price":11.00,"desc":"Zingy lemon sorbet served in a frozen lemon shell with a sugar rim and mint sprig.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F9647dbfc-28fe-46d6-ab3b-a96db2ecd2eb.jpg"},
    {"id":409,"name":"Dragon Fruit Ice Cream",      "price":14.00,"desc":"Exotic dragon fruit ice cream in a vivid pink dragon fruit shell with black chocolate seeds.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F5fa109c4-b39b-4a5a-ac9c-cc4df8a1f84a.jpg"},
    {"id":410,"name":"Kiwi Ice Cream Shape",        "price":12.00,"desc":"Kiwi sorbet shaped as a halved kiwi with white chocolate centre and tiny chocolate seeds.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F35fe021b-52e0-410b-8259-b0a184b2d056.jpg"},
    {"id":411,"name":"Banana Ice Cream",            "price":11.00,"desc":"Creamy banana ice cream shaped and coloured like a real banana with a chocolate dip tip.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2Fa7dbd8e3-1084-4e3a-b396-aef54956496f.jpg"},
    {"id":412,"name":"Cherry Ice Cream",            "price":12.00,"desc":"Sweet cherry sorbet moulded into twin cherries on a green candy stem. Adorable and delicious.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2Fc3919731-ad47-47ee-a15d-36f86ef325c1.jpg"},
    {"id":413,"name":"Orange Creamsicle Shape",     "price":12.00,"desc":"Orange sorbet and vanilla cream inside a perfectly shaped orange with leaf detail.","img":"https://media.pixverse.ai/pixverse%2Fi2i%2Fori%2Fa53d8893-bfae-4f43-a5b7-061fba068703.jpg"},
    {"id":414,"name":"Apple Ice Cream",             "price":12.00,"desc":"Green apple sorbet in a red apple shape with caramel centre and marzipan leaf and stem.","img":"https://media.pixverse.ai/pixverse%2Fi2i%2Fori%2Fa6c81d36-20a8-4288-b2c2-c6b0478a99b8.jpg"},
    {"id":415,"name":"Raspberry Shape Ice Cream",   "price":13.00,"desc":"Raspberry sorbet in a realistic raspberry cluster shape — tart, juicy and gorgeous.","img":"https://media.pixverse.ai/pixverse%2Ft2i%2Fori%2F9132363e-708e-4c22-a252-dba7738c35ff.jpg"},
]

POPSICLES = [
    {"id":501,"name":"Chocolate Dip Bar",           "price":10.00,"desc":"Vanilla ice cream on a stick fully dipped in Belgian dark chocolate shell with almond flakes.","img":"https://static.vecteezy.com/system/resources/previews/007/883/028/non_2x/chocolate-covered-vanilla-ice-cream-with-chocolate-core-filling-popular-food-with-sweet-taste-for-the-hot-summer-3d-rendering-free-photo.jpg"},
    {"id":502,"name":"Mixed Fruit Popsicle",        "price":9.00, "desc":"Layers of strawberry, orange and mango fruit puree frozen on a stick. 100% real fruit.","img":"https://wholelifestylenutrition.com/wp-content/uploads/IMG_9733.jpg"},
    {"id":503,"name":"Rainbow Popsicle",            "price":10.00,"desc":"Six vibrant fruit layers — cherry, orange, lemon, lime, blueberry and grape — in one pop.","img":"https://thefirstyearblog.com/wp-content/uploads/2016/03/Rainbow-Popsicles-4B.jpg"},
    {"id":504,"name":"Yogurt Strawberry Bar",       "price":10.00,"desc":"Creamy Greek yoghurt and strawberry ice bar with granola coating. Guilt-free indulgence.","img":"https://www.jessicagavin.com/wp-content/uploads/2014/05/strawberry-yogurt-popsicles-granola-1200-500x500.jpg"},
    {"id":505,"name":"Coconut Cream Bar",           "price":11.00,"desc":"Rich coconut cream popsicle coated in toasted coconut flakes and white chocolate.","img":"https://sugarfreesprinkles.com/wp-content/uploads/2019/03/coconut-popsicles-5.jpg"},
    {"id":506,"name":"Mango Chilli Popsicle",       "price":10.00,"desc":"Sweet Alphonso mango popsicle with a surprise chilli-lime dusting — sweet heat perfection.","img":"https://www.lindsaypleskot.com/wp-content/uploads/2023/06/Zoomed-Out-Mango-Tajin-Popsciles-with-Lime-1024x1536.jpg"},
    {"id":507,"name":"Cookies & Cream Bar",         "price":11.00,"desc":"Cookies and cream ice cream bar studded with Oreo pieces.","img":"https://assets.unileversolutions.com/v1/1211960.png"},
    {"id":508,"name":"Watermelon Popsicle",         "price":9.00, "desc":"Refreshing real watermelon juice popsicle with chocolate chip seeds. Summer in a stick.","img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRV3mPWpHe0SOuMvK7OWmQ40oKS7DkGScxbag&s"},
    {"id":509,"name":"Salted Caramel Bar",          "price":12.00,"desc":"Caramel ice cream bar with caramel core, dipped in milk chocolate and sea salt.","img":"https://en-chatelaine.mblycdn.com/ench/resized/2025/07/900x900/salted-caramel-ice-cream-bars-recipe.jpg"},
    {"id":510,"name":"Pistachio Icecream Bar",      "price":12.00,"desc":"Pistachio ice cream bars are smooth, nutty, and dipped in a crisp chocolate shell.","img":"https://i.pinimg.com/videos/thumbnails/originals/7f/ac/b8/7facb86e38500552650232a386d3d3dc.0000000.jpg"},
    {"id":511,"name":"Strawberry Cream Bar",        "price":10.00,"desc":"Strawberry and cream double-layer popsicle. Classic flavours perfectly layered.","img":"https://aclassictwist.com/wp-content/uploads/2021/03/Strawberry-and-Cream-Popsicles-2.jpg"},
    {"id":512,"name":"Hazelnut Crunch Bar",         "price":13.00,"desc":"Ferrero-inspired hazelnut ice cream bar coated in milk chocolate and chopped hazelnuts.","img":"https://i.pinimg.com/1200x/ed/ab/a5/edaba567ab369d6d563f28868731ee0a.jpg"},
    {"id":513,"name":"Passion Fruit Bar",           "price":11.00,"desc":"Tangy passion fruit sorbet bar with a mango core — tropical and intensely fruity.","img":"https://i.pinimg.com/736x/4e/f5/c8/4ef5c8bf4d44b9e7674691e744196e5b.jpg"},
    {"id":514,"name":"Bubblegum Pop",               "price":9.00, "desc":"Bright pink bubblegum flavoured popsicle with rainbow candy pieces inside.","img":"https://i.pinimg.com/1200x/91/dc/d9/91dcd99f5b05b19ac1c193e359dfe992.jpg"},
    {"id":515,"name":"Espresso Almond Bar",         "price":13.00,"desc":"Intense espresso ice cream bar with almond brittle coating and chocolate dip.","img":"https://www.saltandserenity.com/wp-content/uploads/2025/06/Angle-hero-in-focus-and-remove.mov.00_01_11_15.Still001-1-683x1024.jpg"},
]

SUNDAES = [
    {"id":601,"name":"Classic Chocolate Sundae",    "price":22.00,"base":"Chocolate","toppings":["Hot fudge","Whipped cream","Maraschino cherry","Chocolate sprinkles"],"desc":"The timeless sundae — rich chocolate ice cream drowning in hot fudge, crowned with whipped cream and a cherry.","img":"https://www.keep-calm-and-eat-ice-cream.com/wp-content/uploads/2020/10/Chocolate-sundae-square.png"},
    {"id":602,"name":"Caramel Dream Sundae",        "price":23.00,"base":"Vanilla","toppings":["Caramel sauce","Toffee pieces","Whipped cream","Sea salt flakes"],"desc":"Vanilla ice cream drenched in salted caramel sauce with chewy toffee pieces and a sea salt finish.","img":"https://thescranline.com/wp-content/uploads/2021/10/Caramel-Apple-Sundae-IGWEB-05.jpg"},
    {"id":603,"name":"Banana Split",               "price":26.00,"base":"Vanilla, Chocolate, Strawberry","toppings":["Hot fudge","Strawberry sauce","Caramel","Whipped cream","Banana","3 cherries"],"desc":"The legendary banana split — three scoops across a split banana with three sauces, whipped cream and cherries.","img":"https://www.cookefast.com/wp-content/uploads/2025/01/banana-split-sundae.png"},
    {"id":604,"name":"Brownie Sundae",             "price":28.00,"base":"Vanilla","toppings":["Warm brownie","Hot fudge","Whipped cream","Chocolate chips","Powdered sugar"],"desc":"A warm fudgy brownie buried under vanilla ice cream, hot fudge and whipped cream. Pure comfort in a bowl.","img":"https://bakesbychichi.com/wp-content/uploads/2015/05/DSC_1274.jpg"},
    {"id":605,"name":"Berry Blast Sundae",         "price":24.00,"base":"Strawberry","toppings":["Mixed berries","Berry coulis","Whipped cream","Granola","Mint"],"desc":"Strawberry ice cream with a tumble of fresh mixed berries, berry coulis and crunchy granola.","img":"https://i.pinimg.com/736x/75/cf/f1/75cff18ab9650cd1ad3e0167df09b70a.jpg"},
    {"id":606,"name":"Oreo Monster Sundae",        "price":26.00,"base":"Cookies & Cream","toppings":["Crushed Oreos","Oreo cream","Hot fudge","Whipped cream","Whole Oreo"],"desc":"For serious Oreo lovers — cookies and cream ice cream buried in Oreo crumbles and cream.","img":"https://i.pinimg.com/1200x/93/ac/35/93ac351cf873f2b06230d9b5e8417f35.jpg"},
    {"id":607,"name":"Mango Tango Sundae",         "price":23.00,"base":"Mango","toppings":["Fresh mango","Mango coulis","Coconut flakes","Whipped cream","Lime zest"],"desc":"Mango ice cream with fresh mango chunks, mango coulis and coconut flakes. Tropical paradise.","img":"https://i.pinimg.com/736x/ae/ed/ab/aeedabc515f31b2fa55db90dc78d8267.jpg"},
    {"id":608,"name":"Peanut Butter Cup Sundae",   "price":27.00,"base":"Chocolate","toppings":["Peanut butter sauce","Reese's pieces","Hot fudge","Whipped cream","Peanuts"],"desc":"Chocolate ice cream with peanut butter sauce and Reese's pieces. Salty-sweet perfection.","img":"https://i.pinimg.com/736x/c9/1b/0d/c91b0d9a66821f0b571622c516bf3eff.jpg"},
    {"id":609,"name":"Waffle Sundae",              "price":28.00,"base":"Vanilla","toppings":["Fresh waffle","Maple syrup","Whipped cream","Butter","Berries"],"desc":"A crispy golden waffle topped with vanilla ice cream, maple syrup and fresh berries. Breakfast meets dessert.","img":"https://www.prairiefarms.com/wp-content/uploads/files/2023/WaffleSundae.jpg"},
    {"id":610,"name":"Tiramisu Sundae",            "price":27.00,"base":"Coffee","toppings":["Espresso shot","Mascarpone","Ladyfinger","Cocoa powder","Coffee syrup"],"desc":"Coffee ice cream with espresso, mascarpone cream and crumbled ladyfingers — tiramisu deconstructed.","img":"https://i.pinimg.com/1200x/29/05/57/29055792618bf836645d4c3d067ef46f.jpg"},
    {"id":611,"name":"Tropical Sundae",            "price":24.00,"base":"Coconut","toppings":["Pineapple chunks","Mango salsa","Coconut flakes","Passion fruit","Lime"],"desc":"Coconut ice cream with a tropical fruit medley and passion fruit drizzle. Holiday in a glass.","img":"https://thumbs.dreamstime.com/b/tropical-ice-cream-sundae-coconut-shell-served-beachside-enjoy-refreshing-crafted-mango-pineapple-flavors-361552981.jpg"},
    {"id":612,"name":"S'mores Sundae",             "price":26.00,"base":"Chocolate","toppings":["Toasted marshmallow","Graham cracker","Hot fudge","Chocolate chips","Campfire caramel"],"desc":"Chocolate ice cream with toasted marshmallow, graham cracker crumble and hot fudge. Campfire vibes.","img":"https://chocolatewithgrace.com/wp-content/uploads/2022/05/Smores-Sundaes-edit-3-1-of-1-scaled.jpg"},
    {"id":613,"name":"Pistachio Honey Sundae",     "price":25.00,"base":"Pistachio","toppings":["Warm honey","Rose petals","Crushed pistachios","Whipped cream","Cardamom"],"desc":"Pistachio ice cream drizzled with warm honey and rose petals — a Middle Eastern-inspired masterpiece.","img":"https://lovelydelites.com/wp-content/uploads/2024/08/IMG_4525-480x270.jpg"},
    {"id":614,"name":"Nutella Sundae",             "price":26.00,"base":"Hazelnut","toppings":["Warm Nutella","Banana","Crushed hazelnuts","Whipped cream","Chocolate flakes"],"desc":"Hazelnut ice cream with warm Nutella, fresh banana and crushed hazelnuts. Dreamy.","img":"https://snapcalorie-webflow-website.s3.us-east-2.amazonaws.com/media/food_pics_v2/medium/nutella_sundae.jpg"},
    {"id":615,"name":"Rainbow Candy Sundae",       "price":23.00,"base":"Vanilla","toppings":["Rainbow sprinkles","Gummy bears","Pop rocks","Whipped cream","Candy floss"],"desc":"Vanilla ice cream loaded with every candy topping imaginable. Pure fun in a bowl — kids go wild!","img":"https://i.pinimg.com/736x/a4/27/e7/a427e74015b77b1b79cbd2e405b895a9.jpg"},
]

SPECIALS = [
    {"id":701,"name":"Thai Rolled Ice Cream",       "price":28.00,"desc":"Ice cream base poured on a -20°C plate and rolled into perfect scrolls. Choose your flavour and toppings. Made fresh in 90 seconds.","img":"https://gdb.voanews.com/31ac14c2-f576-48c6-a164-acd5839e439f_cx0_cy6_cw0_w1080_h608_s.jpg"},
    {"id":702,"name":"Pistachio Gelato",            "price":16.00,"desc":"Authentic Italian-style pistachio gelato made with Bronte DOP pistachios. Dense, creamy and intensely nutty.","img":"https://www.cuisinart.com/dw/image/v2/ABAF_PRD/on/demandware.static/-/Sites-us-cuisinart-sfra-Library/default/dwd5ffb62c/images/recipe-Images/pistachio-gelato-recipe.jpg?sw=1200&sh=1200&sm=fit"},
    {"id":703,"name":"Chocolate Hazelnut Gelato",   "price":16.00,"desc":"Rich bacio gelato — Italian chocolate and hazelnut — smooth, intense and impossibly creamy.","img":"https://mygerman.recipes/wp-content/uploads/2022/07/Chocolate-hazelnut-ice-cream-3-of-6-1200x800.jpg"},
    {"id":704,"name":"Frozen Yogurt Bowl",          "price":18.00,"desc":"Tart frozen yoghurt served in a bowl with granola, fresh berries, honey and chia seeds. Light and healthy.","img":"https://tropeaka.com.au/cdn/shop/articles/protein-berry-froyo-bowl_ce0ee081-a8ae-4d79-bb9b-13ee82b5b302_900x.jpg?v=1571786031"},
    {"id":705,"name":"Mochi Ice Cream 6pk",         "price":32.00,"desc":"Six Japanese mochi balls — chewy rice dough filled with ice cream. Flavours: matcha, mango, strawberry, chocolate, vanilla, sesame.","img":"https://i.pinimg.com/736x/d4/08/b8/d408b830940ec00141e4601462057873.jpg"},
    {"id":706,"name":"Classic Vanilla Milkshake",   "price":20.00,"desc":"Thick and creamy vanilla milkshake blended with premium ice cream and whole milk. Topped with whipped cream.","img":"https://potatorolls.com/wp-content/uploads/Sundae_Vanilla-960x640.jpg"},
    {"id":707,"name":"Oreo Cookies Milkshake",      "price":22.00,"desc":"Oreo ice cream milkshake blended with real Oreo cookies, topped with whipped cream and an Oreo on the rim.","img":"https://saltandbaker.com/wp-content/uploads/2020/12/oreo-milkshake-recipe.jpg"},
    {"id":708,"name":"Strawberry Milkshake",        "price":20.00,"desc":"Fresh strawberry ice cream milkshake with real strawberry pieces and a strawberry-dipped rim.","img":"https://www.butteredsideupblog.com/wp-content/uploads/2023/06/How-to-Make-a-Strawberry-Milkshake-Without-Ice-Cream-17-scaled.jpg"},
    {"id":709,"name":"Ice Cream Sandwich",          "price":15.00,"desc":"Two freshly baked cookies sandwiching a generous scoop of ice cream. Roll edges in sprinkles or chocolate chips.","img":"https://www.twistandmake.com/hs-fs/hubfs/twist-and-make-images/New-Twist-and-Make-Recipes/640-Images/56-oreo-ice-cream-sandwich.jpg?width=640&height=640&name=56-oreo-ice-cream-sandwich.jpg"},
    {"id":710,"name":"Nutella Crepe Ice Cream",     "price":25.00,"desc":"Thin golden crepe filled with Nutella and two scoops of vanilla gelato, rolled and dusted with powdered sugar.","img":"https://i.pinimg.com/736x/70/ef/c3/70efc332d383252b7dc39373b6b05ebe.jpg"},
    {"id":711,"name":"Lemon Sorbet",                "price":14.00,"desc":"Italian-style lemon sorbet served in a frozen lemon shell. Intensely citrusy, dairy-free, refreshing.","img":"https://i.pinimg.com/736x/50/69/47/506947cdc1bada8b5db578f9cbd289de.jpg"},
    {"id":712,"name":"Boba Ice Cream",              "price":22.00,"desc":"Ice cream topped with tapioca boba pearls and your choice of flavoured syrup. The fusion trend you need to try.","img":"https://i.pinimg.com/1200x/58/75/5d/58755db7f850341bc8bfb0a91d292f8f.jpg"},
    {"id":713,"name":"Deep Fried Ice Cream",        "price":26.00,"desc":"Vanilla ice cream ball in a crispy golden corn flake crust, fried to order. Hot outside, cold inside.","img":"https://i.pinimg.com/1200x/e7/47/bd/e747bd0498673f6f279a17b45890f9d0.jpg"},
    {"id":714,"name":"Affogato",                    "price":18.00,"desc":"A shot of hot espresso poured over a scoop of vanilla gelato. Italian elegance in its simplest form.","img":"https://i.pinimg.com/1200x/28/55/48/28554803efed00b2ab22cbdc17f1927d.jpg"},
    {"id":715,"name":"Churro Ice Cream Cup",        "price":24.00,"desc":"Crispy churro pieces with cinnamon sugar served in a cup with vanilla ice cream and chocolate dipping sauce.","img":"https://i.pinimg.com/1200x/af/62/fb/af62fb758de4e6643102c72b2ecb982f.jpg"},
    {"id":716,"name":"Nitrogen Ice Cream",          "price":30.00,"desc":"Ice cream made fresh with liquid nitrogen right in front of you. Pick your base, flavour and mix-ins. Theatre and taste.","img":"https://i.pinimg.com/1200x/71/ae/f3/71aef3ec405fdb9749afef578fb63bd4.jpg"},
]

ALL_PRODUCTS = CONES + CUPS + CAKES + FRUITSHAPED + POPSICLES + SUNDAES + SPECIALS

def get_product(pid):
    return next((p for p in ALL_PRODUCTS if p["id"] == pid), None)

def cart_count():
    return sum(session.get("cart", {}).values())

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, address TEXT, phone TEXT,
        items TEXT, total REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit(); conn.close()

init_db()

# ─── ROUTES ───

@app.route("/")
def home():
    featured = [CONES[0], SUNDAES[2], CAKES[0], SPECIALS[4]]
    return render_template("home.html", featured=featured, cart_count=cart_count())

@app.route("/cones")
def cones():
    return render_template("category.html", title="Cone Ice Creams", icon="🍦", products=CONES, cat="cones", cart_count=cart_count())

@app.route("/cups")
def cups():
    return render_template("category.html", title="Cup Ice Creams", icon="🍨", products=CUPS, cat="cups", cart_count=cart_count())

@app.route("/cakes")
def cakes():
    return render_template("cakes.html", title="Ice Cream Cakes", icon="🎂", products=CAKES, cart_count=cart_count())

@app.route("/fruit-shaped")
def fruit_shaped():
    return render_template("category.html", title="Fruit-Shaped Ice Creams", icon="🍉", products=FRUITSHAPED, cat="fruit-shaped", cart_count=cart_count())

@app.route("/popsicles")
def popsicles():
    return render_template("category.html", title="Popsicles & Ice Bars", icon="🍡", products=POPSICLES, cat="popsicles", cart_count=cart_count())

@app.route("/sundaes")
def sundaes():
    return render_template("sundaes.html", title="Sundae Ice Creams", icon="🍧", products=SUNDAES, cart_count=cart_count())

@app.route("/specials")
def specials():
    return render_template("category.html", title="Special Ice Creams", icon="✨", products=SPECIALS, cat="specials", cart_count=cart_count())

@app.route("/cart")
def cart_page():
    cart = session.get("cart", {})
    items, subtotal = [], 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            lt = p["price"] * qty
            subtotal += lt
            items.append({"product": p, "qty": qty, "line_total": lt})
    delivery = 15.00 if items else 0
    return render_template("cart.html", items=items, subtotal=subtotal, delivery=delivery, total=subtotal+delivery, cart_count=cart_count())

@app.route("/checkout", methods=["GET","POST"])
def checkout():
    cart = session.get("cart", {})
    items, subtotal = [], 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            lt = p["price"] * qty
            subtotal += lt
            items.append({"product": p, "qty": qty, "line_total": lt})
    delivery = 15.00 if items else 0
    total = subtotal + delivery
    if request.method == "POST":
        name = request.form.get("name","").strip()
        address = request.form.get("address","").strip()
        phone = request.form.get("phone","").strip()
        if name and address and phone and items:
            conn = sqlite3.connect(DB)
            conn.execute("INSERT INTO orders (name,address,phone,items,total) VALUES (?,?,?,?,?)",
                (name, address, phone,
                 json.dumps([{"name":i["product"]["name"],"qty":i["qty"],"price":i["product"]["price"]} for i in items]),
                 total))
            conn.commit(); conn.close()
            items_count = sum(cart.values())
            session["cart"] = {}
            session["last_order"] = {"name":name,"total":total,"items_count":items_count}
            return redirect(url_for("order_success"))
    return render_template("checkout.html", items=items, subtotal=subtotal, delivery=delivery, total=total, cart_count=cart_count())

@app.route("/order-success")
def order_success():
    order = session.get("last_order", {})
    return render_template("success.html", order=order, cart_count=0)

@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    data = request.get_json()
    pid = str(data.get("id"))
    p = get_product(int(pid))
    if not p: return jsonify({"error":"Not found"}), 404
    cart = session.get("cart", {})
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart
    return jsonify({"success":True,"cart_count":sum(cart.values()),"message":f"{p['name']} added!"})

@app.route("/api/cart/update", methods=["POST"])
def api_cart_update():
    data = request.get_json()
    pid = str(data.get("id"))
    qty = int(data.get("qty", 0))
    cart = session.get("cart", {})
    if qty <= 0: cart.pop(pid, None)
    else: cart[pid] = qty
    session["cart"] = cart
    return jsonify({"success":True,"cart_count":sum(cart.values())})

@app.route("/api/cart/remove", methods=["POST"])
def api_cart_remove():
    data = request.get_json()
    pid = str(data.get("id"))
    cart = session.get("cart", {})
    cart.pop(pid, None)
    session["cart"] = cart
    return jsonify({"success":True,"cart_count":sum(cart.values())})

if __name__ == "__main__":
    app.run(debug=True, port=5002)