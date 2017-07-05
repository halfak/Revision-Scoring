from ....dependencies import DependentSet
from ...feature import Feature
from ...meta import aggregators, bools
from .diff import Diff

class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.datasources = revision_datasources

        self.sitelinks = aggregators.len(self.datasources.sitelinks)
        "`int` : A count of sitelinks in the revision"
        self.labels = aggregators.len(self.datasources.labels)
        "`int` : A count of labels in the revision"
        self.aliases = aggregators.len(self.datasources.aliases)
        "`int` : A count of aliases in the revision"
        self.descriptions = aggregators.len(self.datasources.descriptions)
        "`int` : A count of descriptions in the revision"
        self.properties = aggregators.len(self.datasources.properties)
        "`int` : A count of properties in the revision"
        self.claims = aggregators.len(self.datasources.claims)
        "`int` : A count of claims in the revision"
        self.sources = aggregators.len(self.datasources.sources)
        "`int` : A count of sources in the revision"
        self.qualifiers = aggregators.len(self.datasources.qualifiers)
        "`int` : A count of qualifiers in the revision"
        self.badges = aggregators.len(self.datasources.badges)
        "`int` : A count of badges in the revision"
        self.external_sources_ratio = self.datasources.external_sources_ratio 
        "`float` : A ratio/division between number of external references and number of claims that have reference(s) in the revision"
        self.unique_sources = aggregators.len(self.datasources.unique_sources)  
        "`int` : A count of unique sources in the revision" 
        self.complete_translations = aggregators.len(self.datasources.complete_translations)
        "`int` :A count of completed translations (a pair of completed label and description) in the revision" 
        self.complete_important_translations = self.datasources.complete_important_translations 
        "`float` : A ratio of completed important translations (a pair of completed label and description) in the revision"
        self.image_quality = self.datasources.image_quality 
        "`float` : Megapixels of the image in the revision"
        self.all_sources = aggregators.len(self.datasources.all_sources)
        "`int` : A count of all sources in the revision" 
        self.all_wikimedia_sources = aggregators.len(self.datasources.all_wikimedia_sources)
        "`int` : A count of all sources which come from Wikimedia projects in the revision" 
        self.all_external_sources = self.datasources.all_external_sources
        "`int` : A count of all sources which do not come from Wikimedia projects in the revision" 

        if hasattr(self.datasources, "parent"):
            self.parent = Revision(name + ".parent", self.datasources.parent)
            """
            :class:`revscoring.features.wikibase.Revision` : The
            parent (aka "previous") revision of the page.
            """

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(name + ".diff", self.datasources.diff)
            """
            :class:`~revscoring.features.wikibase.Diff` : The
            difference between this revision and the parent revision.
            """

    def has_property(self, property, name=None):
        """
        Returns True if the specified property exists

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            name : `str`
                A name to associate with the feature.  If not set, the
                feature's name will be 'has_property(<property>)'
        """
        if name is None:
            name = self._name + ".has_property({0})".format(repr(property))

        return bools.item_in_set(property, self.datasources.properties,
                                 name=name)

    def has_property_value(self, property, value, name=None):
        """
        Returns True if the specified property matches the provided value.

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            value : `mixed`
                The value to match
            name : `str`
                A name to associate with the Feature. If not set, the
                feature's name will be
                'has_property_value(<property>, <value>)'
        """
        if name is None:
            name = self._name + ".has_property_value({0}, {1})" \
                                 .format(repr(property), repr(value))

        return HasPropertyValue(name, property, value, self.datasources.item)


class HasPropertyValue(Feature):
    def __init__(self, name, property, value, item_datasource):
        self.property = property
        self.value = value
        super().__init__(name, self._process, returns=bool,
                         depends_on=[item_datasource])

    def _process(self, item):
        values = item.claims.get(self.property, [])
        return self.value in (i.target for i in values)
