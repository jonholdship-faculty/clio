export const planningRecords = [
  {
    id: 1,
    applicationNumber: 'PA/2023/001',
    decisionDate: '2023-03-15',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Planning Application',
    status: 'Approved',
    description: 'Single-story rear extension to residential property',
    details: 'Application for a 3m deep single-story rear extension to a semi-detached property in a conservation area. Approved with conditions regarding materials used and construction hours.'
  },
  {
    id: 2,
    applicationNumber: 'PA/2023/018',
    decisionDate: '2023-05-22',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Planning Application',
    status: 'Rejected',
    description: 'Conversion of residential property to HMO',
    details: 'Application to convert a 3-bedroom house to a 6-bedroom House in Multiple Occupation. Rejected due to concerns about overcrowding, insufficient amenity space, and impact on parking in the local area.'
  },
  {
    id: 3,
    applicationNumber: 'EA/2023/007',
    decisionDate: '2023-07-10',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Enforcement',
    status: 'Active',
    description: 'Unauthorized construction activity',
    details: 'Enforcement action regarding unauthorized construction work outside permitted hours and not in accordance with approved plans from PA/2023/001. Ongoing investigation with site visits scheduled.'
  },
  {
    id: 4,
    applicationNumber: 'AP/2023/004',
    decisionDate: '2023-08-05',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Appeal',
    status: 'Pending',
    description: 'Appeal against rejection of HMO conversion',
    details: 'Appeal lodged against the rejection of PA/2023/018. Appellant argues that the proposed HMO would not have significant impacts on the local area and that sufficient measures were included to address concerns about amenity space and parking.'
  },
  {
    id: 5,
    applicationNumber: 'EA/2022/033',
    decisionDate: '2022-11-15',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Enforcement',
    status: 'Resolved',
    description: 'Unauthorized signage on listed building',
    details: 'Enforcement action regarding installation of illuminated signage on a Grade II listed building without consent. Case resolved with removal of signage and subsequent application for appropriate non-illuminated signage.'
  },
  {
    id: 6,
    applicationNumber: 'PA/2022/097',
    decisionDate: '2022-09-30',
    address: '14 High Street, London, SW1A 1AB',
    type: 'Planning Application',
    status: 'Approved with Conditions',
    description: 'Change of use from retail to café',
    details: 'Application for change of use from A1 retail to A3 café/restaurant. Approved with conditions regarding opening hours, waste management, and extraction systems to mitigate impact on neighboring residential properties.'
  },
  {
    id: 7,
    applicationNumber: 'AP/2022/018',
    decisionDate: '2022-12-10',
    address: '15 Queen Street, London, SW1A 2BC',
    type: 'Appeal',
    status: 'Rejected',
    description: 'Appeal against conditions for restaurant conversion',
    details: 'Appeal against conditions imposed on PA/2022/097, specifically regarding restricted opening hours. Appeal rejected as inspector determined that the conditions were reasonable to protect residential amenity in the area.'
  },
  {
    id: 8,
    applicationNumber: 'AP/2023/009',
    decisionDate: '2023-09-15',
    address: '12 High Street, London, SW1A 1AA',
    type: 'Appeal',
    status: 'Approved',
    description: 'Appeal against rejection of dormer window',
    details: 'Appeal against rejection of planning application for a dormer window on the front elevation. Appeal approved as inspector determined that the design would not harm the character of the conservation area.'
  }
];

export const aiSummaries = {
  enforcement: 'Two enforcement actions in the past 18 months. One case resolved, with an active investigation into non-compliant building works.',
  appeals: 'Three appeals against planning decisions made. One approved (dormer window), one rejected (HMO conversion), and one pending.',
  planningAppeals: 'Application approval rate of 33% is below the borough average of 45%. Concerns about overdevelopment in conservation area.'
}; 