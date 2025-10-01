from nd_python.endpoints.manage import EpFabricDetailGet

# pylint: disable=protected-access


class TestEpFabricDetailGet:
    """Test cases for EpFabricDetailGet endpoint class"""

    def test_init_default_values(self):
        """Test that EpFabricDetailGet initializes with correct default values"""
        ep = EpFabricDetailGet()

        assert ep.verb == "GET"
        assert ep.path == "/api/v1/manage/fabrics"
        assert ep.description == "Get Fabric Details"
        assert ep._category == "fabric"
        assert ep.query_filter is not None

    def test_fabric_name_property_getter_setter(self):
        """Test fabric_name property getter and setter"""
        ep = EpFabricDetailGet()

        # Test setter
        ep.fabric_name = "my_fabric"

        # Test getter
        assert ep.fabric_name == "my_fabric"

    def test_commit_without_query_filter(self):
        """Test commit() method without any query filter parameters"""
        ep = EpFabricDetailGet()
        ep.commit()

        # Should only have the category parameter
        assert ep.path == "/api/v1/manage/fabrics?category=fabric"

    def test_commit_with_filter_only(self):
        """Test commit() with only filter parameter set"""
        ep = EpFabricDetailGet()
        ep.query_filter.filter = "name:my_fabric"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "filter=name%3Amy_fabric" in ep.path

    def test_commit_with_all_query_parameters(self):
        """Test commit() with all query filter parameters set"""
        ep = EpFabricDetailGet()
        ep.query_filter.filter = "name:my_fabric"
        ep.query_filter.max = 10
        ep.query_filter.offset = 5
        ep.query_filter.sort = "name"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "filter=name%3Amy_fabric" in ep.path
        assert "max=10" in ep.path
        assert "offset=5" in ep.path
        assert "sort=name" in ep.path

    def test_commit_with_max_and_offset(self):
        """Test commit() with max and offset parameters"""
        ep = EpFabricDetailGet()
        ep.query_filter.max = 20
        ep.query_filter.offset = 10
        ep.commit()

        assert "category=fabric" in ep.path
        assert "max=20" in ep.path
        assert "offset=10" in ep.path

    def test_commit_with_sort_ascending(self):
        """Test commit() with sort parameter (ascending)"""
        ep = EpFabricDetailGet()
        ep.query_filter.sort = "name"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "sort=name" in ep.path

    def test_commit_with_sort_descending(self):
        """Test commit() with sort parameter (descending)"""
        ep = EpFabricDetailGet()
        ep.query_filter.sort = "-name"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "sort=-name" in ep.path

    def test_commit_with_multiple_sort_fields(self):
        """Test commit() with multiple sort fields"""
        ep = EpFabricDetailGet()
        ep.query_filter.sort = "name,-timestamp"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "sort=name%2C-timestamp" in ep.path

    def test_commit_with_complex_filter(self):
        """Test commit() with complex Lucene-style filter"""
        ep = EpFabricDetailGet()
        ep.query_filter.filter = "name:my_fabric AND status:active"
        ep.commit()

        assert "category=fabric" in ep.path
        assert "filter=name%3Amy_fabric+AND+status%3Aactive" in ep.path

    def test_commit_idempotent(self):
        """Test that calling commit() multiple times is idempotent"""
        ep = EpFabricDetailGet()
        ep.query_filter.filter = "name:fabric1"
        ep.query_filter.max = 5

        ep.commit()
        first_path = ep.path

        ep.commit()
        second_path = ep.path

        assert first_path == second_path

    def test_query_filter_instance(self):
        """Test that query_filter is a QueryFilterGeneric instance"""
        ep = EpFabricDetailGet()

        # Verify we can set properties on query_filter
        ep.query_filter.filter = "test:value"
        ep.query_filter.max = 100
        ep.query_filter.offset = 50
        ep.query_filter.sort = "field1,-field2"

        assert ep.query_filter.filter == "test:value"
        assert ep.query_filter.max == 100
        assert ep.query_filter.offset == 50
        assert ep.query_filter.sort == "field1,-field2"

    def test_base_path_unchanged_before_commit(self):
        """Test that path is not modified before commit() is called"""
        ep = EpFabricDetailGet()
        ep.query_filter.filter = "name:fabric"

        # Before commit, path should be base path
        assert ep.path == "/api/v1/manage/fabrics"

    def test_path_includes_category_after_commit(self):
        """Test that path always includes category parameter after commit"""
        ep = EpFabricDetailGet()
        ep.commit()

        assert ep.path.startswith("/api/v1/manage/fabrics?category=fabric")

    def test_fabric_name_independent_of_query_filter(self):
        """Test that fabric_name property is independent of query_filter"""
        ep = EpFabricDetailGet()
        ep.fabric_name = "my_fabric"
        ep.query_filter.filter = "status:active"

        # fabric_name doesn't automatically add to query_filter
        ep.commit()
        assert ep.fabric_name == "my_fabric"
        # Only the explicitly set filter should be in the path
        assert "filter=status%3Aactive" in ep.path
