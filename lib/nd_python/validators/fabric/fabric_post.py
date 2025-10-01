"""Pydantic v2 model for ND fabric POST payload."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Location(BaseModel):
    """Fabric location coordinates."""

    latitude: float = 0
    longitude: float = 0


class IdRange(BaseModel):
    """Generic ID range with start and end values."""

    start: int
    end: int


class FlowRuleAttributes(BaseModel):
    """Flow rule attributes for telemetry collection."""

    bidirectional: bool = False
    dst_ip: str | None = Field(None, alias="dstIp")
    dst_port: str | None = Field(None, alias="dstPort")
    protocol: str | None = None
    src_ip: str | None = Field(None, alias="srcIp")
    src_port: str | None = Field(None, alias="srcPort")


class InterfaceCollection(BaseModel):
    """Interface collection configuration."""

    interfaces: list[str]
    switch_name: str | None = Field(None, alias="switchName")


class L3OutInterfaceCollection(BaseModel):
    """L3Out interface collection configuration."""

    encap: str | None = None
    interfaces: list[str]
    l3_out: str | None = Field(None, alias="l3Out")
    switch_id: str | None = Field(None, alias="switchId")
    switch_name: str | None = Field(None, alias="switchName")
    tenant: str | None = None


class InterfaceFlowRule(BaseModel):
    """Interface flow rule configuration."""

    attributes: list[FlowRuleAttributes]
    interface_collection: list[InterfaceCollection] = Field(alias="interfaceCollection")
    name: str
    subnets: list[str]
    type: str = "physical"


class L3OutFlowRule(BaseModel):
    """L3Out flow rule configuration."""

    interface_collection: list[L3OutInterfaceCollection] = Field(alias="interfaceCollection")
    name: str
    subnets: list[str]
    type: str = "subInterface"


class VrfFlowRule(BaseModel):
    """VRF flow rule configuration."""

    attributes: list[FlowRuleAttributes]
    name: str
    subnets: list[str]
    tenant: str
    vrf: str


class FlowRules(BaseModel):
    """Flow rules configuration."""

    interface_flow_rules: list[InterfaceFlowRule] = Field(alias="interfaceFlowRules")
    l3_out_flow_rules: list[L3OutFlowRule] = Field(alias="l3OutFlowRules")
    vrf_flow_rules: list[VrfFlowRule] = Field(alias="vrfFlowRules")


class FlowCollectionModes(BaseModel):
    """Flow collection modes configuration."""

    flow_telemetry: bool = Field(False, alias="flowTelemetry")
    net_flow: bool = Field(False, alias="netFlow")
    s_flow: bool = Field(False, alias="sFlow")


class FlowCollection(BaseModel):
    """Flow collection configuration."""

    flow_collection_modes: FlowCollectionModes = Field(alias="flowCollectionModes")
    flow_rules: FlowRules = Field(alias="flowRules")
    traffic_analytics: bool = Field(False, alias="trafficAnalytics")


class CollectionSettings(BaseModel):
    """Collection settings for telemetry."""

    advisories: list[str] | None = None
    anomalies: list[str] | None = None
    audit_logs: list[str] | None = Field(None, alias="auditLogs")
    faults: list[str] | None = None
    risk_and_conformance_reports: list[str] | None = Field(None, alias="riskAndConformanceReports")
    statistics: list[str] | None = None


class EmailSettings(BaseModel):
    """Email settings for telemetry collection."""

    collection_frequency_in_days: int = Field(0, alias="collectionFrequencyInDays")
    collection_settings: CollectionSettings = Field(alias="collectionSettings")
    format: str = "html"
    name: str
    only_include_active_alerts: bool = Field(False, alias="onlyIncludeActiveAlerts")
    receiver_email: EmailStr = Field(alias="receiverEmail")
    start_date: datetime = Field(alias="startDate")


class MessageBusSettings(BaseModel):
    """Message bus settings for telemetry collection."""

    collection_settings: CollectionSettings = Field(alias="collectionSettings")
    collection_type: str = Field("alertsAndEvents", alias="collectionType")
    server: str


class MicroburstSettings(BaseModel):
    """Microburst settings for telemetry."""

    microburst: bool = False
    sensitivity: str = "low"


class ExportSettings(BaseModel):
    """Export settings for NAS telemetry."""

    export_format: str = Field("json", alias="exportFormat")
    export_type: str = Field("full", alias="exportType")


class NasSettings(BaseModel):
    """NAS settings for telemetry collection."""

    export_settings: ExportSettings = Field(alias="exportSettings")
    server: str


class SustainabilitySettings(BaseModel):
    """Sustainability settings for telemetry."""

    cost: float


class SyslogCollectionSettings(BaseModel):
    """Syslog collection settings."""

    anomalies: list[str]


class SyslogSettings(BaseModel):
    """Syslog settings for telemetry collection."""

    collection_settings: SyslogCollectionSettings = Field(alias="collectionSettings")
    facility: str
    servers: list[str]


class AnalysisSettings(BaseModel):
    """Analysis settings for telemetry."""

    is_enabled: bool = Field(False, alias="isEnabled")


class TelemetrySettings(BaseModel):
    """Telemetry settings configuration."""

    analysis_settings: AnalysisSettings = Field(alias="analysisSettings")
    email: list[EmailSettings]
    flow_collection: FlowCollection = Field(alias="flowCollection")
    message_bus: list[MessageBusSettings] = Field(alias="messageBus")
    microburst: MicroburstSettings
    nas: NasSettings
    sustainability: SustainabilitySettings
    syslog: SyslogSettings


class Management(BaseModel):
    """Fabric management configuration."""

    aaa: bool = False
    advanced_ssh_option: bool = Field(False, alias="advancedSshOption")
    advertise_physical_ip: bool = Field(False, alias="advertisePhysicalIp")
    advertise_physical_ip_on_border: bool = Field(True, alias="advertisePhysicalIpOnBorder")
    aiml_qos: bool = Field(False, alias="aimlQos")
    aiml_qos_policy: str = Field("400G", alias="aimlQosPolicy")
    allow_l3_vni_no_vlan: bool = Field(True, alias="allowL3VniNoVlan")
    anycast_border_gateway_advertise_physical_ip: bool = Field(False, alias="anycastBorderGatewayAdvertisePhysicalIp")
    anycast_gateway_mac: str = Field("2020.0000.00aa", alias="anycastGatewayMac")
    anycast_loopback_id: int = Field(10, alias="anycastLoopbackId")
    anycast_rendezvous_point_ip_range: str = Field("10.254.254.0/24", alias="anycastRendezvousPointIpRange")
    auto_bgp_neighbor_description: bool = Field(True, alias="autoBgpNeighborDescription")
    auto_symmetric_default_vrf: bool = Field(False, alias="autoSymmetricDefaultVrf")
    auto_symmetric_vrf_lite: bool = Field(False, alias="autoSymmetricVrfLite")
    auto_unique_vrf_lite_ip_prefix: bool = Field(False, alias="autoUniqueVrfLiteIpPrefix")
    auto_vrf_lite_default_vrf: bool = Field(False, alias="autoVrfLiteDefaultVrf")
    bfd: bool = False
    bfd_authentication: bool = Field(False, alias="bfdAuthentication")
    bfd_authentication_key: str = Field("string", alias="bfdAuthenticationKey")
    bfd_authentication_key_id: int = Field(100, alias="bfdAuthenticationKeyId")
    bfd_ibgp: bool = Field(False, alias="bfdIbgp")
    bfd_isis: bool = Field(False, alias="bfdIsis")
    bfd_ospf: bool = Field(False, alias="bfdOspf")
    bfd_pim: bool = Field(False, alias="bfdPim")
    bgp_asn: str = Field("65002", alias="bgpAsn")
    bgp_authentication: bool = Field(False, alias="bgpAuthentication")
    bgp_authentication_key: str = Field("string", alias="bgpAuthenticationKey")
    bgp_authentication_key_type: str = Field("3des", alias="bgpAuthenticationKeyType")
    bgp_loopback_id: int = Field(0, alias="bgpLoopbackId")
    bgp_loopback_ip_range: str = Field("10.2.0.0/22", alias="bgpLoopbackIpRange")
    bgp_loopback_ipv6_range: str = Field("fd00::a02:0/119", alias="bgpLoopbackIpv6Range")
    bootstrap_multi_subnet: str = Field("", alias="bootstrapMultiSubnet")
    brownfield_network_name_format: str = Field("Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$", alias="brownfieldNetworkNameFormat")
    brownfield_skip_overlay_network_attachments: bool = Field(False, alias="brownfieldSkipOverlayNetworkAttachments")
    cdp: bool = False
    copp_policy: str = Field("strict", alias="coppPolicy")
    day0_bootstrap: bool = Field(False, alias="day0Bootstrap")
    default_private_vlan_secondary_network_template: str = Field("Pvlan_Secondary_Network", alias="defaultPrivateVlanSecondaryNetworkTemplate")
    default_queuing_policy: bool = Field(False, alias="defaultQueuingPolicy")
    default_queuing_policy_cloudscale: str = Field("queuing_policy_default_8q_cloudscale", alias="defaultQueuingPolicyCloudscale")
    default_queuing_policy_other: str = Field("queuing_policy_default_other", alias="defaultQueuingPolicyOther")
    default_queuing_policy_r_series: str = Field("queuing_policy_default_r_series", alias="defaultQueuingPolicyRSeries")
    default_vrf_redistribution_bgp_route_map: str = Field("extcon-rmap-filter", alias="defaultVrfRedistributionBgpRouteMap")
    dhcp_protocol_version: str = Field("dhcpv4", alias="dhcpProtocolVersion")
    extra_config_aaa: str = Field("string", alias="extraConfigAaa")
    extra_config_intra_fabric_links: str = Field("string", alias="extraConfigIntraFabricLinks")
    extra_config_leaf: str = Field("string", alias="extraConfigLeaf")
    extra_config_nxos_bootstrap: str = Field("string", alias="extraConfigNxosBootstrap")
    extra_config_spine: str = Field("string", alias="extraConfigSpine")
    extra_config_tor: str = Field("string", alias="extraConfigTor")
    fabric_interface_type: str = Field("p2p", alias="fabricInterfaceType")
    fabric_mtu: int = Field(9216, alias="fabricMtu")
    fabric_vpc_domain_id: bool = Field(False, alias="fabricVpcDomainId")
    fabric_vpc_qos: bool = Field(False, alias="fabricVpcQos")
    fabric_vpc_qos_policy_name: str = Field("spine_qos_for_fabric_vpc_peering", alias="fabricVpcQosPolicyName")
    greenfield_debug_flag: str = Field("disable", alias="greenfieldDebugFlag")
    host_interface_admin_state: bool = Field(True, alias="hostInterfaceAdminState")
    inband_dhcp_servers: str = Field("1.35.8.241", alias="inbandDhcpServers")
    inband_management: bool = Field(False, alias="inbandManagement")
    interface_statistics_load_interval: int = Field(10, alias="interfaceStatisticsLoadInterval")
    intra_fabric_subnet_range: str = Field("10.4.0.0/16", alias="intraFabricSubnetRange")
    ip_service_level_agreement_id_range: IdRange = Field(alias="ipServiceLevelAgreementIdRange")
    ipv6_anycast_rendezvous_point_ip_range: str = Field("fd00::254:254:0/118", alias="ipv6AnycastRendezvousPointIpRange")
    ipv6_link_local: bool = Field(True, alias="ipv6LinkLocal")
    ipv6_multicast_group_subnet: str = Field("ff1e::/121", alias="ipv6MulticastGroupSubnet")
    ipv6_subnet_range: str = Field("fd00::a04:0/112", alias="ipv6SubnetRange")
    ipv6_subnet_target_mask: int = Field(126, alias="ipv6SubnetTargetMask")
    isis_area_number: str = Field("0001", alias="isisAreaNumber")
    isis_authentication: bool = Field(False, alias="isisAuthentication")
    isis_authentication_key: str = Field("string", alias="isisAuthenticationKey")
    isis_authentication_keychain_key_id: int = Field(127, alias="isisAuthenticationKeychainKeyId")
    isis_authentication_keychain_name: str = Field("string", alias="isisAuthenticationKeychainName")
    isis_level: str = Field("level-2", alias="isisLevel")
    isis_overload: bool = Field(True, alias="isisOverload")
    isis_overload_elapse_time: int = Field(60, alias="isisOverloadElapseTime")
    isis_point_to_point: bool = Field(True, alias="isisPointToPoint")
    l2_host_interface_mtu: int = Field(9216, alias="l2HostInterfaceMtu")
    l2_vni_range: IdRange = Field(alias="l2VniRange")
    l3_vni_ipv6_multicast_group: str = Field("ff1e::", alias="l3VniIpv6MulticastGroup")
    l3vni_multicast_group: str = Field("239.1.1.0", alias="l3vniMulticastGroup")
    l3_vni_no_vlan_default_option: bool = Field(False, alias="l3VniNoVlanDefaultOption")
    l3_vni_range: IdRange = Field(alias="l3VniRange")
    leaf_to_r_id_range: bool = Field(False, alias="leafToRIdRange")
    leaf_tor_vpc_port_channel_id_range: IdRange = Field(alias="leafTorVpcPortChannelIdRange")
    link_state_routing_protocol: str = Field("ospf", alias="linkStateRoutingProtocol")
    link_state_routing_tag: str = Field("UNDERLAY", alias="linkStateRoutingTag")
    local_dhcp_server: bool = Field(False, alias="localDhcpServer")
    macsec: bool = False
    macsec_algorithm: str = Field("AES_128_CMAC", alias="macsecAlgorithm")
    macsec_cipher_suite: str = Field("GCM-AES-XPN-256", alias="macsecCipherSuite")
    macsec_fallback_algorithm: str = Field("AES_128_CMAC", alias="macsecFallbackAlgorithm")
    macsec_fallback_key_string: str = Field("B9DC20D30ef3E0aA6AD4fFdDa3bb59c9e1471d035Af3eE024E781b7DaEd764AB297Ec9cE6c3BEDbEC9eA64Ca79bF1d2", alias="macsecFallbackKeyString")
    macsec_key_string: str = Field("E6dFCE84Ff518d5a89beFbCF66efaF9c54DE5b3F9a4A8DD9467a5fEe6", alias="macsecKeyString")
    macsec_report_timer: int = Field(5, alias="macsecReportTimer")
    management_ipv4_prefix: int = Field(24, alias="managementIpv4Prefix")
    management_ipv6_prefix: int = Field(64, alias="managementIpv6Prefix")
    mpls_handoff: bool = Field(False, alias="mplsHandoff")
    mpls_isis_area_number: str = Field("0001", alias="mplsIsisAreaNumber")
    mpls_loopback_identifier: int = Field(101, alias="mplsLoopbackIdentifier")
    mpls_loopback_ip_range: str = Field("10.101.0.0/25", alias="mplsLoopbackIpRange")
    mst_instance_range: str = Field("0", alias="mstInstanceRange")
    multicast_group_subnet: str = Field("239.1.1.0/25", alias="multicastGroupSubnet")
    mvpn_vrf_route_import_id_range: int = Field(65535, alias="mvpnVrfRouteImportIdRange")
    network_extension_template: str = Field("Default_Network_Extension_Universal", alias="networkExtensionTemplate")
    network_template: str = Field("Default_Network_Universal", alias="networkTemplate")
    network_vlan_range: IdRange = Field(alias="networkVlanRange")
    next_generation_oam: bool = Field(True, alias="nextGenerationOAM")
    nve_hold_down_timer: int = Field(180, alias="nveHoldDownTimer")
    nve_loopback_id: int = Field(1, alias="nveLoopbackId")
    nve_loopback_ip_range: str = Field("10.3.0.0/22", alias="nveLoopbackIpRange")
    nve_loopback_ipv6_range: str = Field("fd00::a03:0/118", alias="nveLoopbackIpv6Range")
    nxapi: bool = False
    nxapi_http: bool = Field(False, alias="nxapiHttp")
    nxapi_http_port: int = Field(80, alias="nxapiHttpPort")
    nxapi_https_port: int = Field(443, alias="nxapiHttpsPort")
    object_tracking_number_range: IdRange = Field(alias="objectTrackingNumberRange")
    ospf_area_id: str = Field("0.0.0.0", alias="ospfAreaId")
    ospf_authentication: bool = Field(False, alias="ospfAuthentication")
    ospf_authentication_key: str = Field("string", alias="ospfAuthenticationKey")
    ospf_authentication_key_id: int = Field(127, alias="ospfAuthenticationKeyId")
    overlay_mode: str = Field("cli", alias="overlayMode")
    performance_monitoring: bool = Field(False, alias="performanceMonitoring")
    per_vrf_loopback_auto_provision: bool = Field(False, alias="perVrfLoopbackAutoProvision")
    per_vrf_loopback_auto_provision_ipv6: bool = Field(False, alias="perVrfLoopbackAutoProvisionIpv6")
    per_vrf_loopback_ip_range: str = Field("10.5.0.0/22", alias="perVrfLoopbackIpRange")
    per_vrf_loopback_ipv6_range: str = Field("fd00::a05:0/112", alias="perVrfLoopbackIpv6Range")
    phantom_rendezvous_point_loopback_id1: int = Field(2, alias="phantomRendezvousPointLoopbackId1")
    phantom_rendezvous_point_loopback_id2: int = Field(3, alias="phantomRendezvousPointLoopbackId2")
    phantom_rendezvous_point_loopback_id3: int = Field(4, alias="phantomRendezvousPointLoopbackId3")
    phantom_rendezvous_point_loopback_id4: int = Field(5, alias="phantomRendezvousPointLoopbackId4")
    pim_hello_authentication: bool = Field(False, alias="pimHelloAuthentication")
    pim_hello_authentication_key: str = Field("string", alias="pimHelloAuthenticationKey")
    policy_based_routing: bool = Field(False, alias="policyBasedRouting")
    power_redundancy_mode: str = Field("redundant", alias="powerRedundancyMode")
    priority_flow_control_watch_interval: int = Field(1000, alias="priorityFlowControlWatchInterval")
    private_vlan: bool = Field(False, alias="privateVlan")
    ptp: bool = False
    ptp_vlan_id: int = Field(3967, alias="ptpVlanId")
    quantum_key_distribution: bool = Field(False, alias="quantumKeyDistribution")
    quantum_key_distribution_profile_name: str = Field("string", alias="quantumKeyDistributionProfileName")
    real_time_backup: bool = Field(True, alias="realTimeBackup")
    real_time_interface_statistics_collection: bool = Field(False, alias="realTimeInterfaceStatisticsCollection")
    rendezvous_point_count: int = Field(2, alias="rendezvousPointCount")
    rendezvous_point_loopback_id: int = Field(254, alias="rendezvousPointLoopbackId")
    rendezvous_point_mode: str = Field("asm", alias="rendezvousPointMode")
    replication_mode: str = Field("multicast", alias="replicationMode")
    route_map_sequence_number_range: IdRange = Field(alias="routeMapSequenceNumberRange")
    route_reflector_count: int = Field(2, alias="routeReflectorCount")
    router_id_range: str = Field("10.2.0.0/23", alias="routerIdRange")
    scheduled_backup: bool = Field(True, alias="scheduledBackup")
    scheduled_backup_time: str = Field("00:00", alias="scheduledBackupTime")
    security_group_tag: bool = Field(False, alias="securityGroupTag")
    security_group_tag_id_range: IdRange = Field(alias="securityGroupTagIdRange")
    security_group_tag_prefix: str = Field("SG_", alias="securityGroupTagPrefix")
    security_group_tag_preprovision: bool = Field(False, alias="securityGroupTagPreprovision")
    service_network_vlan_range: IdRange = Field(alias="serviceNetworkVlanRange")
    shared_vpc_domain_id: int = Field(1, alias="sharedVpcDomainId")
    skip_certificate_verification: bool = Field(False, alias="skipCertificateVerification")
    snmp_trap: bool = Field(True, alias="snmpTrap")
    static_underlay_ip_allocation: bool = Field(False, alias="staticUnderlayIpAllocation")
    stp_bridge_priority: int = Field(0, alias="stpBridgePriority")
    stp_root_option: str = Field("unmanaged", alias="stpRootOption")
    stp_vlan_range: str = Field("1-3967", alias="stpVlanRange")
    strict_config_compliance_mode: bool = Field(False, alias="strictConfigComplianceMode")
    sub_interface_dot1q_range: IdRange = Field(alias="subInterfaceDot1qRange")
    target_subnet_mask: int = Field(30, alias="targetSubnetMask")
    tcam_allocation: bool = Field(True, alias="tcamAllocation")
    tenant_dhcp: bool = Field(True, alias="tenantDhcp")
    tenant_routed_multicast: bool = Field(False, alias="tenantRoutedMulticast")
    tenant_routed_multicast_ipv6: bool = Field(False, alias="tenantRoutedMulticastIpv6")
    trustpoint_label: str = Field("string", alias="trustpointLabel")
    type: str = "vxlanIbgp"
    underlay_ipv6: bool = Field(False, alias="underlayIpv6")
    un_numbered_bootstrap_lb_id: int = Field(253, alias="unNumberedBootstrapLbId")
    vpc_auto_recovery_timer: int = Field(360, alias="vpcAutoRecoveryTimer")
    vpc_delay_restore_timer: int = Field(150, alias="vpcDelayRestoreTimer")
    vpc_domain_id_range: IdRange = Field(alias="vpcDomainIdRange")
    vpc_ipv6_neighbor_discovery_sync: bool = Field(True, alias="vpcIpv6NeighborDiscoverySync")
    vpc_layer3_peer_router: bool = Field(True, alias="vpcLayer3PeerRouter")
    vpc_peer_keep_alive_option: str = Field("management", alias="vpcPeerKeepAliveOption")
    vpc_peer_link_enable_native_vlan: bool = Field(False, alias="vpcPeerLinkEnableNativeVlan")
    vpc_peer_link_port_channel_id: int = Field(500, alias="vpcPeerLinkPortChannelId")
    vpc_peer_link_vlan: int = Field(3600, alias="vpcPeerLinkVlan")
    vrf_extension_template: str = Field("Default_VRF_Extension_Universal", alias="vrfExtensionTemplate")
    vrf_lite_auto_config: str = Field("manual", alias="vrfLiteAutoConfig")
    vrf_lite_macsec: bool = Field(False, alias="vrfLiteMacsec")
    vrf_lite_subnet_range: str = Field("10.33.0.0/16", alias="vrfLiteSubnetRange")
    vrf_lite_subnet_target_mask: int = Field(30, alias="vrfLiteSubnetTargetMask")
    vrf_route_import_id_reallocation: bool = Field(False, alias="vrfRouteImportIdReallocation")
    vrf_template: str = Field("Default_VRF_Universal", alias="vrfTemplate")
    vrf_vlan_range: IdRange = Field(alias="vrfVlanRange")


class Meta(BaseModel):
    """ND Fabric metadata."""

    allowed_actions: list[str] = Field(alias="allowedActions")


class FabricPostConfig(BaseModel):
    """ND Fabric POST payload model."""

    license_tier: str = Field("premier", alias="licenseTier")
    location: Location
    management: Management
    meta: Meta
    name: str
    security_domain: str = Field("all", alias="securityDomain")
    telemetry_collection: bool = Field(False, alias="telemetryCollection")
    telemetry_collection_type: str = Field("outOfBand", alias="telemetryCollectionType")
    telemetry_settings: TelemetrySettings = Field(alias="telemetrySettings")
    telemetry_source_interface: str = Field("string", alias="telemetrySourceInterface")
    telemetry_source_vrf: str = Field("string", alias="telemetrySourceVrf")
    telemetry_streaming_protocol: str = Field("ipv4", alias="telemetryStreamingProtocol")

    model_config = ConfigDict()
    model_config["validate_by_name"] = True
    model_config["use_enum_values"] = True


config = list[FabricPostConfig]
