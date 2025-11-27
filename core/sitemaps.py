from django.contrib.sitemaps import Sitemap
from django.urls import reverse, NoReverseMatch
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject
from contents.models import ContentMaterial, FreeContentMasterCategory, FreeContentSubCategory


class StaticPublicViewSitemap(Sitemap):
    """
    Sitemap ONLY for 100% public views that do not require login.
    """

    priority = 0.9
    changefreq = "daily"
    protocol = "https"

    def items(self):
        public_url_names = [
            "home",
            "login",
            "users:register",
            "academic_directory:university_list",
            "search:search_home",
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


class UniversitySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return University.objects.all()

    def location(self, obj):
        return reverse("academic_directory:branch_list", kwargs={"university_slug": obj.slug})


class BranchSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Branch.objects.select_related("university").all()

    def location(self, obj):
        return reverse(
            "academic_directory:degree_list",
            kwargs={
                "university_slug": obj.university.slug,
                "branch_slug": obj.slug
            }
        )


class DegreeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Degree.objects.select_related("branch__university").all()

    def location(self, obj):
        return reverse(
            "academic_directory:academic_year_list",
            kwargs={
                "university_slug": obj.branch.university.slug,
                "branch_slug": obj.branch.slug,
                "degree_slug": obj.slug
            }
        )


class AcademicYearSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return AcademicYear.objects.select_related("degree__branch__university").all()

    def location(self, obj):
        return reverse(
            "academic_directory:subject_list",
            kwargs={
                "university_slug": obj.degree.branch.university.slug,
                "branch_slug": obj.degree.branch.slug,
                "degree_slug": obj.degree.slug,
                "year": obj.year
            }
        )


class SubjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Subject.objects.select_related(
            "academic_year__degree__branch__university"
        ).all()

    def location(self, obj):
        return reverse(
            "academic_directory:public_content_list",
            kwargs={
                "university_slug": obj.academic_year.degree.branch.university.slug,
                "branch_slug": obj.academic_year.degree.branch.slug,
                "degree_slug": obj.academic_year.degree.slug,
                "year": obj.academic_year.year,
                "subject_slug": obj.slug
            }
        )


class PublicContentMaterialSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return ContentMaterial.objects.filter(is_public=True)

    def lastmod(self, obj):
        return obj.updated_at


class FreeContentCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return FreeContentMasterCategory.objects.all()


class FreeContentSubCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return FreeContentSubCategory.objects.select_related("master_category").all()
