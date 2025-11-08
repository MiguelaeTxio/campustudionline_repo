from django.contrib.sitemaps import Sitemap
from django.urls import reverse, NoReverseMatch


class StaticPublicViewSitemap(Sitemap):
    """
    Sitemap ONLY for 100% public views that do not require login.
    """

    priority = 0.9
    changefreq = "daily"
    protocol = "https"

    def items(self):
        public_url_names = [
            "inicio",
            "login",
            "users:register",
        ]
        valid_items = []
        for item_name in public_url_names:
            try:
                reverse(item_name)
                valid_items.append(item_name)
            except NoReverseMatch:
                print(
                    f"ADVERTENCIA (Sitemap): La URL pública con nombre '{item_name}' no se pudo resolver y será omitida."
                )
        return valid_items

    def location(self, item):
        return reverse(item)
