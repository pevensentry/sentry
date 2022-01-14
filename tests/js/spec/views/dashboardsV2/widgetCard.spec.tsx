import {initializeOrg} from 'sentry-test/initializeOrg';
import {mountWithTheme, screen, userEvent} from 'sentry-test/reactTestingLibrary';

import * as modal from 'sentry/actionCreators/modal';
import {Client} from 'sentry/api';
import {DisplayType, Widget, WidgetType} from 'sentry/views/dashboardsV2/types';
import WidgetCard from 'sentry/views/dashboardsV2/widgetCard';

describe('Dashboards > WidgetCard', function () {
  const initialData = initializeOrg({
    organization: TestStubs.Organization({
      features: ['connect-discover-and-dashboards', 'dashboards-edit', 'discover-basic'],
      projects: [TestStubs.Project()],
    }),
    router: {orgId: 'orgId'},
  } as Parameters<typeof initializeOrg>[0]);

  const multipleQueryWidget: Widget = {
    title: 'Errors',
    interval: '5m',
    displayType: DisplayType.LINE,
    widgetType: WidgetType.DISCOVER,
    queries: [
      {
        conditions: 'event.type:error',
        fields: ['count()', 'failure_count()'],
        name: 'errors',
        orderby: '',
      },
      {
        conditions: 'event.type:default',
        fields: ['count()', 'failure_count()'],
        name: 'default',
        orderby: '',
      },
    ],
  };
  const selection = {
    projects: [1],
    environments: ['prod'],
    datetime: {
      period: '14d',
      start: null,
      end: null,
      utc: false,
    },
  };

  const api = new Client();

  beforeEach(function () {
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/events-stats/',
      body: [],
    });
    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/events-geo/',
      body: [],
    });
  });

  afterEach(function () {
    MockApiClient.clearMockResponses();
  });

  it('renders with Open in Discover button and opens the Query Selector Modal when clicked', async function () {
    const spy = jest.spyOn(modal, 'openDashboardWidgetQuerySelectorModal');
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={multipleQueryWidget}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Open in Discover')).toBeInTheDocument();
    userEvent.click(screen.getByText('Open in Discover'));
    expect(spy).toHaveBeenCalledWith({
      organization: initialData.organization,
      widget: multipleQueryWidget,
    });
  });

  it('renders with Open in Discover button and opens in Discover when clicked', async function () {
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{...multipleQueryWidget, queries: [multipleQueryWidget.queries[0]]}}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Open in Discover')).toBeInTheDocument();
    expect(screen.getByText('Open in Discover').closest('a')).toHaveAttribute(
      'href',
      '/organizations/org-slug/discover/results/?environment=prod&field=count%28%29&field=failure_count%28%29&name=Errors&project=1&query=event.type%3Aerror&statsPeriod=14d&yAxis=count%28%29&yAxis=failure_count%28%29'
    );
  });

  it('Opens in Discover with World Map', async function () {
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.WORLD_MAP,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Open in Discover')).toBeInTheDocument();
    expect(screen.getByText('Open in Discover').closest('a')).toHaveAttribute(
      'href',
      '/organizations/org-slug/discover/results/?display=worldmap&environment=prod&field=geo.country_code&field=count%28%29&name=Errors&project=1&query=event.type%3Aerror%20has%3Ageo.country_code&statsPeriod=14d&yAxis=count%28%29'
    );
  });

  it('Opens in Discover with Top N', async function () {
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.TOP_N,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Open in Discover')).toBeInTheDocument();
    expect(screen.getByText('Open in Discover').closest('a')).toHaveAttribute(
      'href',
      '/organizations/org-slug/discover/results/?display=top5&environment=prod&field=count%28%29&name=Errors&project=1&query=event.type%3Aerror&statsPeriod=14d&yAxis=count%28%29'
    );
  });

  it('calls onDuplicate when Duplicate Widget is clicked', async function () {
    const mock = jest.fn();
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.WORLD_MAP,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={mock}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Duplicate Widget')).toBeInTheDocument();
    userEvent.click(screen.getByText('Duplicate Widget'));
    expect(mock).toHaveBeenCalledTimes(1);
  });

  it('does not add duplicate widgets if max widget is reached', async function () {
    const mock = jest.fn();
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.WORLD_MAP,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={() => undefined}
        onDuplicate={mock}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Duplicate Widget')).toBeInTheDocument();
    userEvent.click(screen.getByText('Duplicate Widget'));
    expect(mock).toHaveBeenCalledTimes(0);
  });

  it('calls onEdit when Edit Widget is clicked', async function () {
    const mock = jest.fn();
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.WORLD_MAP,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={() => undefined}
        onEdit={mock}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Edit Widget')).toBeInTheDocument();
    userEvent.click(screen.getByText('Edit Widget'));
    expect(mock).toHaveBeenCalledTimes(1);
  });

  it('renders delete widget option', async function () {
    const mock = jest.fn();
    mountWithTheme(
      <WidgetCard
        api={api}
        organization={initialData.organization}
        widget={{
          ...multipleQueryWidget,
          displayType: DisplayType.WORLD_MAP,
          queries: [{...multipleQueryWidget.queries[0], fields: ['count()']}],
        }}
        selection={selection}
        isEditing={false}
        onDelete={mock}
        onEdit={() => undefined}
        onDuplicate={() => undefined}
        renderErrorMessage={() => undefined}
        isSorting={false}
        currentWidgetDragging={false}
        showContextMenu
        widgetLimitReached={false}
      />
    );

    await tick();

    userEvent.click(screen.getByTestId('context-menu'));
    expect(screen.getByText('Delete Widget')).toBeInTheDocument();
  });
});